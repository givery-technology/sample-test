name := """sample-test-impl"""

version := "1.0-SNAPSHOT"

lazy val root = (project in file(".")).enablePlugins(PlayScala)

scalaVersion := "2.11.6"

libraryDependencies ++= Seq(
  "org.scalikejdbc" %% "scalikejdbc" % "2.2.7",
  "org.scalikejdbc" %% "scalikejdbc-config" % "2.2.7",
  "org.scalikejdbc" %% "scalikejdbc-play-initializer" % "2.4.0",
  "org.xerial" % "sqlite-jdbc" % "3.8.11.1",
  cache
)

resolvers += "scalaz-bintray" at "http://dl.bintray.com/scalaz/releases"

// Play provides two styles of routers, one expects its actions to be injected, the
// other, legacy style, accesses its actions statically.
routesGenerator := InjectedRoutesGenerator
