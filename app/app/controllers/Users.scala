package controllers

import play.api._
import play.api.Play.current
import play.api.mvc._
import scalikejdbc._
import play.api.libs.json.Json
import play.api.libs.json.JsObject
import play.api.data._
import play.api.data.Forms._
import play.api.cache.Cache

class Users extends Controller {

  def events = Action { implicit request =>
    Form(tuple(
      "from" -> nonEmptyText,
      "offset" -> optional(number),
      "limit" -> optional(number)
    )).bindFromRequest.fold(
      hasErrors = form => BadRequest,
      success = { case (from, offsetOp, limitOp) =>
        val offset = offsetOp.getOrElse(0)
        val limit = limitOp.getOrElse(20)
        if (offset < 0 || limit <= 0) {
          BadRequest
        } else {
          DB.localTx { implicit session =>
            val events = sql"""
              SELECT
                A.id as event_id,
                A.name as event_name,
                A.start_date,
                B.id as company_id,
                B.name as company_name
              FROM 
                events A, 
                users B
              WHERE A.user_id = B.id
                AND A.start_date >= ${from}
              ORDER BY
                A.start_date
              LIMIT ${limit} OFFSET ${offset}
            """.map{ rs =>
              Json.obj(
                "id" -> rs.int("event_id"),
                "name" -> rs.string("event_name"),
                "start_date" -> rs.string("start_date"),
                "company" -> Json.obj(
                  "id" -> rs.int("company_id"),
                  "name" -> rs.string("company_name")
                )
              )
            }.list.apply
            Ok(Json.obj(
              "code" -> 200,
              "events" -> events
            ))
          }
        }
      }
    ) 
  }

  def reserve = Action { implicit request =>
    Form(tuple(
      "token" -> text,
      "event_id" -> number,
      "reserve" -> boolean
    )).bindFromRequest.fold(
      hasErrors = form => BadRequest,
      success = { case (token, event_id, reserve) =>
        Cache.getAs[JsObject]("session." + token).filter { user =>
          val group_id = (user \ "group_id").as[Int]
          group_id == 1
        }.map { user =>
          val user_id = (user \ "id").as[Int]
          DB.localTx { implicit session =>
            val reserved = sql"""
              SELECT COUNT(*) FROM attends
              WHERE user_id = ${user_id}
                AND event_id = ${event_id}
            """.map(_.int(1) == 1).single.apply.getOrElse(false)
            if (reserved) {
              if (reserve) {
                Ok(Json.obj(
                  "code" -> 501,
                  "message" -> "Already reserved"
                ))
              } else {
                SQL("DELETE FROM attends WHERE user_id = ? AND event_id = ?")
                  .bind(user_id, event_id)
                  .update.apply
                Ok(Json.obj(
                  "code" -> 200,
                  "message" -> "Unreserve succeed"
                ))
              }
            } else {
              if (reserve) {
                SQL("INSERT INTO attends (user_id, event_id) VALUES(?, ?)")
                  .bind(user_id, event_id)
                  .update.apply
                Ok(Json.obj(
                  "code" -> 200,
                  "message" -> "Reserve succeed"
                ))
              } else {
                Ok(Json.obj(
                  "code" -> 502,
                  "message" -> "Not reserved"
                ))
              }
            }
          }
        }.getOrElse {
          Ok(Json.obj(
            "code" -> 401,
            "message" -> "Not logined"
          ))
        }
      }
    ) 
  }

}