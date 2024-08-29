import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Property } from './types/types';

const Profile: React.FC = () => {
  const [profile, setProfile] = useState({
    username: '',
    email: '',
    savedProperties: [] as Property[]
  });

  useEffect(() => {
    // Fetch saved properties from your API
    fetch('http://127.0.0.1:5000/profile', {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}` // Assuming you store the token in localStorage
      }
    })
      .then(response => response.json())
      .then(data => setProfile(data));
  }, []);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-3xl font-bold mb-6">Your Profile</h1>
      <div className="bg-white shadow overflow-hidden sm:rounded-lg">
        <div className="px-4 py-5 sm:px-6">
          <h2 className="text-lg leading-6 font-medium text-gray-900">Personal Information</h2>
        </div>
        <div className="border-t border-gray-200">
          <dl>
            <div className="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
              <dt className="text-sm font-medium text-gray-500">Full name</dt>
              <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">{ profile.username } </dd>
            </div>
            <div className="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
              <dt className="text-sm font-medium text-gray-500">Email address</dt>
              <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">{ profile.email }</dd>
            </div>
          </dl>
        </div>
      </div>

      <h2 className="text-2xl font-bold mt-8 mb-4">Saved Properties</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {profile?.savedProperties?.map(property => (
          <div key={property.id} className="bg-white shadow-md rounded-lg overflow-hidden">
            {property.image_urls && property.image_urls.length > 0 && (
              <img src={property.image_urls[0]} alt={property.address} className="w-full h-48 object-cover" />
            )}
            <div className="p-4">
              <h3 className="text-xl font-semibold mb-2">{property.address}</h3>
              <p className="text-gray-600 mb-2">${property.price.toLocaleString()}</p>
              <p className="text-gray-600 mb-4">
                {property.bedrooms} bed | {property.bathrooms} bath | {property.square_footage} sqft
              </p>
              <Link 
                to={`/property/${property.id}`} 
                className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
              >
                View Details
              </Link>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Profile;