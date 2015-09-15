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

class Companies extends Controller {

  def events = Action { implicit request =>
    Form(tuple(
      "token" -> text,
      "from" -> nonEmptyText,
      "offset" -> optional(number),
      "limit" -> optional(number)
    )).bindFromRequest.fold(
      hasErrors = form => BadRequest,
      success = { case (token, from, offsetOp, limitOp) =>
        Cache.getAs[JsObject]("session." + token).filter { user =>
          val group_id = (user \ "group_id").as[Int]
          group_id == 2
        }.map { user =>
          val user_id = (user \ "id").as[Int]
          val offset = offsetOp.getOrElse(0)
          val limit = limitOp.getOrElse(20)
          if (offset < 0 || limit <= 0) {
            BadRequest
          } else {
            DB.localTx { implicit session =>
              val events = sql"""
                SELECT
                  A.id,
                  A.name,
                  A.start_date,
                  COUNT(B.user_id) as number_of_attendees
                FROM 
                  events A
                LEFT OUTER JOIN
                  attends B ON (A.id = B.event_id)
                WHERE A.user_id = ${user_id}
                  AND A.start_date >= ${from}
                GROUP BY 
                  A.id,
                  A.name,
                  A.start_date
                ORDER BY
                  A.start_date
                LIMIT ${limit} OFFSET ${offset}
              """.map{ rs =>
                Json.obj(
                  "id" -> rs.int("id"),
                  "name" -> rs.string("name"),
                  "start_date" -> rs.string("start_date"),
                  "number_of_attendees" -> rs.int("number_of_attendees")
                )
              }.list.apply
              Ok(Json.obj(
                "code" -> 200,
                "events" -> events
              ))
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