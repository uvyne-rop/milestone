import React from 'react';

const EmailTemplate = ({ username, verificationLink }) => {
  return (
    <div className="bg-gray-100 p-8">
      <div className="max-w-lg mx-auto bg-white rounded-lg shadow-lg overflow-hidden">
        <div className="bg-indigo-600 p-4 text-white text-center">
          <h1 className="text-2xl font-bold">Welcome to The Groove!</h1>
        </div>
        <div className="p-6">
          <p className="text-gray-700">
            Hi {username},
          </p>
          <p className="text-gray-700 mt-4">
            Thank you for signing up for The Groove. We're excited to have you on board!
          </p>
          <p className="text-gray-700 mt-4">
            To complete your registration, please verify your email address by clicking the button below:
          </p>
          <div className="mt-6 text-center">
            <a 
              href={verificationLink} 
              className="inline-block bg-indigo-600 text-white py-2 px-4 rounded hover:bg-indigo-700"
            >
              Verify Email
            </a>
          </div>
          <p className="text-gray-700 mt-4">
            If you did not sign up for an account, please ignore this email.
          </p>
          <p className="text-gray-700 mt-4">
            Best regards,<br />
            The Groove Team
          </p>
        </div>
      </div>
    </div>
  );
};

export default EmailTemplate;
