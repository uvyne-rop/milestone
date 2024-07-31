import React from 'react';

function Signup() {
  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="p-6 bg-white rounded shadow-md w-80">
        <h2 className="text-2xl font-bold text-center mb-4">Sign Up</h2>
        <form>
          <div className="mb-4">
            <label className="block text-sm font-bold mb-1" htmlFor="email">
              Email
            </label>
            <input
              className="w-full px-3 py-2 border rounded shadow-sm focus:outline-none focus:ring focus:ring-blue-300"
              type="email"
              id="email"
              placeholder="Enter your email"
            />
          </div>
          <div className="mb-4">
            <label className="block text-sm font-bold mb-1" htmlFor="password">
              Password
            </label>
            <input
              className="w-full px-3 py-2 border rounded shadow-sm focus:outline-none focus:ring focus:ring-blue-300"
              type="password"
              id="password"
              placeholder="Enter your password"
            />
          </div>
          <div className="mb-6">
            <label className="block text-sm font-bold mb-1" htmlFor="confirm-password">
              Confirm Password
            </label>
            <input
              className="w-full px-3 py-2 border rounded shadow-sm focus:outline-none focus:ring focus:ring-blue-300"
              type="password"
              id="confirm-password"
              placeholder="Confirm your password"
            />
          </div>
          <button
            type="submit"
            className="w-full px-4 py-2 font-bold text-white bg-blue-500 rounded hover:bg-blue-700 focus:outline-none focus:bg-blue-700"
          >
            Sign Up
          </button>
        </form>
        <p className="text-sm text-center text-gray-600 mt-4">
          Already have an account? <a href="/login" className="text-blue-500">Login</a>
        </p>
      </div>
    </div>
  );
}

export default Signup;
