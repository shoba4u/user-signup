#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi
import re

form = """
<h1>Sign Up</h1>
<br>
<form method="post" action="/posthandler">
<label> Username:
    <br>
    <input type="text" name="username" value="%(username)s">
    <div style="color: red;">%(username_error)s</div>
    <br>
</label>
<label> Password:
    <br>
    <input type="password" name="password" value="%(password)s">
    <div style="color: red;">%(password_error)s</div>
    <br>
</label>
<label> Verify Password:
    <br>
    <input type="password" name="verify_password" value="%(verify_password)s">
    <div style="color: red;">%(verify_password_error)s</div>
    <br>
</label>
<label> Email (optional):
    <br>
    <input type="email" name="email" value="%(email)s">
    <div style="color: red;">%(email_error)s</div>
    <br>
</label>
    <br>
<input type="submit">
</form>
"""

def html_escape(s):
    #To capture the error 
    return cgi.escape(s, quote = True)

username_verify = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    #Validating username
    return username_verify.match(username)

password_verify = re.compile(r"^.{3,20}$")
def valid_password(password):
    #Validating Password
    return password_verify.match(password)

email_verify = re.compile("^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
    #Validating E-Mail
    return email_verify.match(email)

class MainHandler(webapp2.RequestHandler):
    def write_form(self, username="", username_error="", password="", password_error="",
    verify_password="", verify_password_error="", email="", email_error=""):
        self.response.write(form % {
        "username": username,
        "username_error": username_error,
        "password": password,
        "password_error": password_error,
        "verify_password": verify_password,
        "verify_password_error": verify_password_error,
        "email": email,
        "email_error": email_error})

    def get(self):
        self.write_form()

class PostHandler(MainHandler):
    def post(self):
        username_form = html_escape(self.request.get('username'))
        password_form = html_escape(self.request.get('password'))
        verify_password_form = html_escape(self.request.get('verify_password'))
        email_form = html_escape(self.request.get('email'))

        username_error = ""
        password_error = ""
        verify_password_error = ""
        email_error = ""


        if not valid_username(username_form):
            username_error = "Please enter a valid username."

        if not valid_password(password_form):
            password_error = "Please enter a valid password."

        if password_form != verify_password_form:
            verify_password_error = "Verification does not match password."

        if  not valid_email(email_form) and email_form != "":
            email_error = "Please enter a valid email."

        if username_error != "" or password_error != "" or verify_password_error != "" or email_error != "":
            self.write_form(username_form, username_error, password_form,
            password_error, verify_password_form, verify_password_error, email_form)

        else:
            self.response.write("<h1>" + "Welcome, " + username_form + "!" + "</h1>")



app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/posthandler', PostHandler)
], debug=True)
