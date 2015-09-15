package controllers

import play.api._
import play.api.Play.current
import play.api.mvc._
import scalikejdbc._
import play.api.libs.json.Json
import play.api.data._
import play.api.data.Forms._
import play.api.cache.Cache
import scala.concurrent.duration._
import java.util.UUID
import java.security.MessageDigest

class Application extends Controller {

  def index = Action {
    Ok(views.html.index("Your new application is ready."))
  }

  def sha1(str: String): String = {
    val md = MessageDigest.getInstance("SHA-1")
    md.update(str.getBytes)
    md.digest.foldLeft("") { (s, b) => s + "%02x".format(if(b < 0) b + 256 else b) }
  }

  def signin = Action { implicit request =>
    Form(tuple(
      "email" -> text,
      "password" -> text
    )).bindFromRequest.fold(
      hasErrors = form => BadRequest,
      success = { case (email, password) =>
        DB.localTx { implicit session =>
          val user = sql"""
            SELECT
              id,
              name,
              group_id
            FROM 
              users 
            WHERE email = ${email}
              AND password = ${sha1(password)}
          """.map{ rs =>
            Json.obj(
              "id" -> rs.int("id"),
              "name" -> rs.string("name"),
              "group_id" -> rs.int("group_id")
            )
          }.single.apply
          user.map { u =>
            val token = UUID.randomUUID.toString
            Cache.set("session." + token, u, 2 hours)
            Ok(Json.obj(
              "code" -> 200,
              "token" -> token,
              "user" -> u
            ))
          }.getOrElse {
            Ok(Json.obj(
              "code" -> 500
            ))
          }
        }
      }
    ) 
  }
}
