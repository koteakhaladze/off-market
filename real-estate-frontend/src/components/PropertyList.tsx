import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Property } from './types/types';
import PropertyMap from './PropertyMap';

const PropertyList: React.FC = () => {
  const [properties, setProperties] = useState<Property[]>([]);

  useEffect(() => {
    // Fetch properties from your API
    fetch('http://127.0.0.1:5000/properties')
      .then(response => response.json())
      .then(data => setProperties(data));
  }, []);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <h1 className="text-3xl font-bold my-8">Explore Properties</h1>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        <PropertyMap properties={properties} />
        {properties.map(property => (
          <Link to={`/property/${property.id}`} key={property.id} className="group">
            <div className="bg-white rounded-lg shadow-md overflow-hidden transition-transform duration-300 group-hover:scale-105">
              <img 
                src={`https://source.unsplash.com/480x360/?house,property&sig=${property.id}`} 
                alt={property.address} 
                className="w-full h-48 object-cover"
              />
              <div className="p-4">
                <h2 className="text-xl font-semibold text-gray-800">{property.address}</h2>
                <p className="text-gray-600 mt-2">${property.price.toLocaleString()} • {property.bedrooms} bed • {property.bathrooms} bath</p>
                <p className="text-gray-500 mt-1">{property.square_footage} sq ft</p>
              </div>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
};

export default PropertyList;