subject = {
   "resetPassword" : "Reset Your Password on Study Buddy",
    "emailSignUpVerification" : "Verify Your Email Address to Complete Your Signup!",
    "newEmailVerification" : "Verify Your New Email Address for Study Buddy"
}

body = {
    "resetPassword" : """Hi {},

We received a request to reset the password for your Study Buddy account. If you made this request, click the link below to reset your password:

Reset Password Link: http://127.0.0.1:8000/forgot-password-byEmail?token={}

This link is valid for 1 hour. If you didn't request a password reset, you can safely ignore this email.

Best regards,  
Study Buddy Support  
testpyprojects@gmail.com""",

    "emailSignUpVerification" : """Hi {},

Thank you for signing up with Study Buddy! To complete your registration, please verify your email address by clicking the link below:

Complete SignUp : http://127.0.0.1:8000/sign-up?token={}

If you didn't sign up for a Study Buddy account, please ignore this email.

Best regards,  
Study Buddy Team  
testpyprojects@gmail.com""",

    "newEmailVerification" : """Hi {},

We received a request to change the email address associated with your Study Buddy account. To verify your new email and complete the process, please click the link below:

Confirmation Link : http://127.0.0.1:8000/forgot-email?token={}

If you did not request this change, you can safely ignore this email. Your email will not be updated unless you verify this change within the next 1 hour.

Thank you for using Study Buddy!
Best regards,
The Study Buddy Team
testpyprojects@gmail.com"""
}

if __name__=='__main__':
    
    print(body["emailSignUpVerification"].format("Hemang Gour", "123456"))