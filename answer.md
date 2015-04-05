# Q5. Refactoring

> If you are a manager of this project and you can change the
specification of this app, what would you do?

I would try to make it more REST-like by using the HTTP status codes
more thoroughly and consistently.

* Don't send a response as `HTTP 200` with a response body of
`{code:401}`. Rather, send `HTTP 401`.

* Send meaningful response codes. For example, a wrong login should
return `HTTP 400 - BAD REQUEST`, since it's an error from which the user
can recover by modifying her input. Currently, the tests expect
`HTTP 500 - INTERNAL SERVER ERROR`, which implies that there's no action
the user can take to fix the problem. The same applies to 
`HTTP 501 - NOT IMPLEMENTED` and `HTTP 502 - BAD GATEWAY`.

If the above is addressed, the use of the `code` key in the response
JSON is redundant. It can be removed or, if there's a need to add
further detail, it could be used for application specific error codes.
I'd add a prefix to those codes to make it apparent that they have a
different meaning.

I would also move the authentication token to the HTTP headers (e.g.
`X-App-Token`). Arguably, the response code and message should also be
in the HTTP headers although it's convenient to leave them in the JSON
response.

Since the API is about events and not so much users and companies, the
endpoints can be refactored to reflect that.

```
GET /api/users/events      => GET /api/events
POST /api/users/reserve    => POST /api/events/{event_id}/[reserve/unreserve]
POST /api/companies/events => GET /api/companies/{company_id}/events
```

Added to that, I would remove some restrictions.
* Why can't a company user see all events?
* Why can't a user see a specific company's events?

I think this is related to the fact that users have a `group_id` key to
differentiante companies and users. Instead, I would have two different
tables for `companies` and `users` and add relationships between them.
e.g. `user X is admin of company Y`. The endpoints should consider
this relationship when granting access or returning data.

