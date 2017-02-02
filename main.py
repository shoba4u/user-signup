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
page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>Signup</title>
    <style type="text/css">
        .error {
            color: red;
        }
    </style>
</head>
<body>
"""
   
page_footer = """
</body>
</html>
"""

USER_VA = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_VA.match(username)

PASS_VA = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_VA.match(password)

EMAIL_VA = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
    return not email or EMAIL_VA.match(email)

class Index(webapp2.RequestHandler):
    def get(self):

        signup_header = "<h1>Signup</h1>"

        username_form = """ 
        <form action="/username" method="post" autocomplete="on">
            <table>
                <tr>
                    <td><label for="username">Username</label></td>
                    <td>
                        <input name="username" type="text" value="" required >
                    </td>
                    
                </tr>
                <tr>
                    <td><label for="password">Password</label></td>
                    <td>
                        <input name="password" type="password" required autocomplete="off">
                    </td>
                    
                </tr>
                <tr>
                    <td><label for="verify">Verify Password</label></td>
                    <td>
                        <input name="verify" type="password" required autocomplete="off">
                    </td>
                    
                </tr>
                <tr>
                    <td><label for="email">Email (optional)</label></td>
                    <td>
                        <input name="email" type="email" value="" >
                    </td>
                    
                </tr>
            </table>
            <input type="submit">
        </form>
        """
         
        # if we have an error, make a <p> to display it
        error = self.request.get("error")
        error_element = "<p class='error'>" + error + "</p>" if error else ""
     

        content = page_header+signup_header+username_form+page_footer+error_element
        self.response.write(content)

class Signup(webapp2.RequestHandler):
    
    def post(self):

        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')


        if not valid_username(username):
            error = "That's not a valid username"
            error_escaped = cgi.escape(error, quote=True)
            self.response.write(error_escaped)
            self.redirect("/?error=" + error_escaped)

        elif not valid_password(password):
            error = "That's not a valid password"
            error_escaped = cgi.escape(error, quote=True)
            self.response.write(error_escaped)
            self.redirect("/?error=" + error_escaped)

        elif password != verify:
            error = "Your passwords didn't match"
            error_escaped = cgi.escape(error, quote=True)
            self.response.write(error_escaped) 
            self.redirect("/?error=" + error_escaped)

        elif not valid_email(email):
            error = "That's not a valid email"
            error_escaped = cgi.escape(error, quote=True)
            self.response.write(error_escaped)
            self.redirect("/?error=" + error_escaped)

        else:
            confirmation = "<h1>" + "Welcome," + username + "</h1>"
            self.response.write(confirmation)
    

app = webapp2.WSGIApplication([
    ('/', Index),
    ('/username',Signup)
], debug=True)
