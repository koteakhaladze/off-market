import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import Map, { Marker, Popup } from 'react-map-gl';
import { Carousel } from 'react-responsive-carousel';
import "react-responsive-carousel/lib/styles/carousel.min.css";
import 'mapbox-gl/dist/mapbox-gl.css';
import { Property } from './types/types';

const MAPBOX_TOKEN = 'pk.eyJ1Ijoia290ZWFraCIsImEiOiJjbTBhdDE2ZG0wMTNiMmtzYzdpMnlkOHVnIn0.3SAE5oT786OCLD5_ziMqOA';

const PropertyList: React.FC = () => {
  const [properties, setProperties] = useState<Property[]>([]);
  const [selectedProperty, setSelectedProperty] = useState<Property | null>(null);
  const [viewState, setViewState] = useState({
    latitude: 37.7749,
    longitude: -122.4194,
    zoom: 11
  });

  useEffect(() => {
    fetch('http://127.0.0.1:5000/properties')
      .then(response => response.json())
      .then(data => setProperties(data));
  }, []);

  if (properties.length === 0) return <div>Loading...</div>;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-3xl font-bold mb-6">Property Listings</h1>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div>
          <Map
            initialViewState={{
              latitude: properties[0]?.latitude || 0,
              longitude: properties[0]?.longitude || 0,
              zoom: 14
            }}
            onMove={evt => setViewState(evt.viewState)}
            style={{width: '100%', height: '400px'}}
            mapStyle="mapbox://styles/mapbox/streets-v11"
            mapboxAccessToken={MAPBOX_TOKEN}
          >
            {properties.map((property) => (
              <Marker
                key={property.id}
                latitude={property.latitude}
                longitude={property.longitude}
                onClick={e => {
                  e.originalEvent.stopPropagation();
                  setSelectedProperty(property);
                }}
              >
              </Marker>
            ))}

            {selectedProperty && (
              <Popup
                latitude={selectedProperty.latitude}
                longitude={selectedProperty.longitude}
                onClose={() => setSelectedProperty(null)}
                closeOnClick={false}
              >
                <div>
                  <h3>{selectedProperty.address}</h3>
                  <p>Price: ${selectedProperty.price.toLocaleString()}</p>
                  <Link to={`/property/${selectedProperty.id}`}>View Details</Link>
                </div>
              </Popup>
            )}
          </Map>
        </div>
        <div className="space-y-8">
          {properties.map(property => (
            <div key={property.id} className="bg-white rounded-lg shadow-md overflow-hidden">
              {property.image_urls && property.image_urls.length > 0 ? (
                <Carousel showThumbs={false} showStatus={false}>
                  {property.image_urls.map((url, index) => (
                    <div key={index}>
                      <img src={url} alt={`Property image ${index + 1}`} className="w-full h-64 object-cover" />
                    </div>
                  ))}
                </Carousel>
              ) : (
                <div className="bg-gray-200 h-64 flex items-center justify-center">
                  <p>No images available</p>
                </div>
              )}
              <div className="p-6">
                <h2 className="text-2xl font-semibold mb-4">{property.address}</h2>
                <p className="text-gray-700 mb-2"><span className="font-semibold">Price:</span> ${property.price.toLocaleString()}</p>
                <p className="text-gray-700 mb-2"><span className="font-semibold">Bedrooms:</span> {property.bedrooms}</p>
                <p className="text-gray-700 mb-2"><span className="font-semibold">Bathrooms:</span> {property.bathrooms}</p>
                <p className="text-gray-700 mb-2"><span className="font-semibold">Square Footage:</span> {property.square_footage} sq ft</p>
                <Link 
                  to={`/property/${property.id}`}
                  className="mt-4 inline-block bg-red-500 text-white py-2 px-4 rounded-lg font-semibold hover:bg-red-600 transition duration-300"
                >
                  View Details
                </Link>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default PropertyList;