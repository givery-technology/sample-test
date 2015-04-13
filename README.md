# Sample Test for new Code-Check

Code-Check is a web service which we are going to develop in 2015.
It provides users the system to make various coding tests and the interface to solve tests.
This is a prototype for it.

## Purpose

- Measuring developing skills of candidates.
- Helping candidates to understand how to develop in Givery.(Using [api-first-spec](https://github.com/shunjikonishi/api-first-spec))
- Considering what the new code-check test should be.

## Test

- We want you to implement some REST APIs by using any languages and frameworks.
- You can see the specification of APIs in [spec](spec) directory.
  - These specs are written with [api-first-spec](https://github.com/shunjikonishi/api-first-spec), and has some API tests.
- Your goal is to develop a web application which be able to pass all these tests.

## How to solve the test
This test requires

- Some web application framework
- MySQL database
- GitHub account(To fork this repository.)

Fork this repository to your GitHub account at first.
And then, develop an application by yourself.

Database structure and sample data are written in [sql/create.sql].  
Build your own mysql server and run this script.

If you want to build it automatically, you can use our [test env builder](https://github.com/code-check/env-builder)

You can set up an environment with following commands.

``` bash
git clone git@github.com:code-check/env-builder.git test-env
cd test-env
cp Vagrantfile.sample Vagrantfile
cp hosts.sample hosts
vagrant up
ansible-playbook all.yml
vagrant ssh
git clone git@github.com:[YOUR GITHUB ACCOUNT]/sample-test.git
mysql -uvagrant -pvagrant -Dvagrant < sample-test/sql/create.sql

cd sample-test
```

And then, implement the app and push to your REPO.

## How to run the api-first-spec test
api-first-spec uses [Mocha](http://mochajs.org/) test framework.

You can run all tests with following commands.

``` bash
cd sample-test
npm install
mocha spec/*
```

Of course you can try runing a single test.

``` bash
mocha spec/users_login.js
```

As default, application settings are defined in [spec/config/config.json](spec/config/config.json).  
You can edit it easy to use.

## Questions
This app is simple event reserve system.

- It has two kind of users.  
  - student
  - company
- All users can see every event list.
(include none logged-in user)
- The student can reserve and unreserve the event.
- The company can see their own event list.

### Q1. Implement login API.
- Login with email and password
- Its response is login token and user data
  - group_id = 1 is student user.
  - group_id = 2 is company user.

### Q2. Implement event_list API for students
- Login is not required
- "from" parameter is required.
  - It specify the date list start from.
- "offset" and "limit" parameter are option.

### Q3. Implement reserve and unreserve API
- Login is required.
- The user must be student.

### Q4. Implement event_list API for companies
- Login is required.
- The user must be company.
- The event information includes the number of attendees.

### Q5. Refactoring
If you are a manager of this project and you can change the specification of this app, what would you do?

Write your opinion to answer.md

## How to submit your answer
- Please let us know about your answer by writing on [issue](https://github.com/code-check/sample-test/issues).
  - Enter "implemented" into the title.
  - Write your repository URL on the comment.

## Support
If you have any questions, please write it to this repository's [issue](https://github.com/code-check/sample-test/issues).

This is experimental case of our new service.  
So, any feedback is welcome!
