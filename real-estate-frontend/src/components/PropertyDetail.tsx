/* eslint-disable jsx-a11y/img-redundant-alt */
import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Property } from './types/types';
import Map from 'react-map-gl';
import { Carousel } from 'react-responsive-carousel';
import { Marker } from 'react-map-gl';
import "react-responsive-carousel/lib/styles/carousel.min.css";
import OfferSubmissionForm from './OfferSubmission';
import RequireAuth from './RequireAuth';
import apiClient, { isLoggedIn } from '../utils/apiClient';

const MAPBOX_TOKEN = 'pk.eyJ1Ijoia290ZWFraCIsImEiOiJjbTBhdDE2ZG0wMTNiMmtzYzdpMnlkOHVnIn0.3SAE5oT786OCLD5_ziMqOA';

const PropertyDetailContent: React.FC = () => {
  const [property, setProperty] = useState<Property | null>(null);
  const { id } = useParams<{ id: string }>();
  const [showOfferForm, setShowOfferForm] = useState(false);
  const [isSaved, setIsSaved] = useState(false);
  console.log(property);

  useEffect(() => {
    const fetchProperties = async () => {
      try {
        const data = await apiClient(`/properties/${id}`);
        setProperty(data);
      } catch (error) {
        console.error('Failed to fetch properties:', error);
      }
    };

    fetchProperties();

    const fetchSavedProperties = async () => {
      try {
        const data = await apiClient(`/saved_properties`);
        setIsSaved(data.filter((p: Property) => p.id === parseInt(id as string)).length > 0);
      } catch (error) {
        console.error('Failed to fetch properties:', error);
      }
    };
    fetchSavedProperties();
  }, [id]);

  const handleSaveProperty = async () => {
    if (!isLoggedIn() || !property) return;

    try {
      const response = await fetch(`http://127.0.0.1:5000/properties/${id}/save`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({ id: property.id })
      });

      if (response.ok) {
        setIsSaved(true);
        alert('Property saved successfully!');
      } else {
        throw new Error('Failed to save property');
      }
    } catch (error) {
      console.error('Error saving property:', error);
      alert('Failed to save property. Please try again.');
    }
  };

  if (!property) return <div>Loading...</div>;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-3xl font-bold mb-6">{property.address}</h1>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div>
          {property.image_urls && property.image_urls.length > 0 ? (
            <Carousel>
              {property.image_urls.map((url, index) => (
                <div key={index}>
                  <img src={url} alt={`Property image ${index + 1}`} />
                </div>
              ))}
            </Carousel>
          ) : (
            <div className="bg-gray-200 h-64 flex items-center justify-center mb-4">
              <p>No images available</p>
            </div>
          )}
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
          {isLoggedIn() && (
            <button 
              className={`w-1/2 mt-6 ${isSaved ? 'bg-green-500 hover:bg-green-600' : 'bg-blue-500 hover:bg-blue-600'} text-white py-3 rounded-lg font-semibold transition duration-300`}
              onClick={handleSaveProperty}
              disabled={isSaved}
            >
              {isSaved ? 'Saved' : 'Save Property'}
            </button>
          )}
          {!property.offer && !showOfferForm ? (
            <button 
              className="w-full mt-6 bg-red-500 text-white py-3 rounded-lg font-semibold hover:bg-red-600 transition duration-300"
              onClick={() => setShowOfferForm(true)}
            >
              Make an Offer
            </button>
          ) : (
            !property.offer && 
            <div className="mt-6">
              <OfferSubmissionForm />
              <button 
                className="w-full mt-6 bg-gray-300 text-gray-700 py-3 rounded-lg font-semibold hover:bg-gray-400 transition duration-300"
                onClick={() => setShowOfferForm(false)}
              >
                Cancel
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

const PropertyDetail: React.FC = () => (
  <RequireAuth>
    <PropertyDetailContent />
  </RequireAuth>
);

export default PropertyDetail;