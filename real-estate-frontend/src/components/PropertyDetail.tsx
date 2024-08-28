import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Property } from './types/types';
import Map from 'react-map-gl';
import { Marker } from 'react-map-gl';

const MAPBOX_TOKEN = 'pk.eyJ1Ijoia290ZWFraCIsImEiOiJjbTBhdDE2ZG0wMTNiMmtzYzdpMnlkOHVnIn0.3SAE5oT786OCLD5_ziMqOA';

const PropertyDetail: React.FC = () => {
  const [property, setProperty] = useState<Property | null>(null);
  const { id } = useParams<{ id: string }>();

  useEffect(() => {
    fetch(`http://127.0.0.1:5000/properties/${id}`)
      .then(response => response.json())
      .then(data => setProperty(data));
  }, [id]);

  if (!property) return <div>Loading...</div>;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-3xl font-bold mb-6">{property.address}</h1>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div>
          <img 
            src={`https://source.unsplash.com/800x600/?house,property&sig=${property.id}`} 
            alt={property.address} 
            className="w-full h-96 object-cover rounded-lg shadow-md"
          />
          <div className="mt-6 bg-white rounded-lg shadow-md p-6">
            <h2 className="text-2xl font-semibold mb-4">Property Details</h2>
            <p className="text-gray-700 mb-2"><span className="font-semibold">Price:</span> ${property.price.toLocaleString()}</p>
            <p className="text-gray-700 mb-2"><span className="font-semibold">Bedrooms:</span> {property.bedrooms}</p>
            <p className="text-gray-700 mb-2"><span className="font-semibold">Bathrooms:</span> {property.bathrooms}</p>
            <p className="text-gray-700 mb-2"><span className="font-semibold">Square Footage:</span> {property.square_footage} sq ft</p>
          </div>
        </div>
        <div>
          <Map
            initialViewState={{
              latitude: property.latitude || 0,
              longitude: property.longitude || 0,
              zoom: 14
            }}
            style={{width: '100%', height: 400}}
            mapStyle="mapbox://styles/mapbox/streets-v11"
            mapboxAccessToken={MAPBOX_TOKEN}
          >
            <Marker
              latitude={property.latitude || 0}
              longitude={property.longitude || 0}
            />
          </Map>
          <button className="w-full mt-6 bg-red-500 text-white py-3 rounded-lg font-semibold hover:bg-red-600 transition duration-300">
            Make an Offer
          </button>
        </div>
      </div>
    </div>
  );
};

export default PropertyDetail;