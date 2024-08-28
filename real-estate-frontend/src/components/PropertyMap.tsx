import React, { useState, useEffect } from 'react';
import Map, { Marker, Popup, NavigationControl, FullscreenControl, GeolocateControl } from 'react-map-gl';
import 'mapbox-gl/dist/mapbox-gl.css';
import { Property } from './types/types';

const MAPBOX_TOKEN = 'pk.eyJ1Ijoia290ZWFraCIsImEiOiJjbTBhdDE2ZG0wMTNiMmtzYzdpMnlkOHVnIn0.3SAE5oT786OCLD5_ziMqOA';

interface PropertyMapProps {
  properties: Property[];
}

const PropertyMap: React.FC<PropertyMapProps> = ({ properties }) => {
  const [viewState, setViewState] = useState({
    latitude: 37.7749,
    longitude: -122.4194,
    zoom: 11
  });
  const [selectedProperty, setSelectedProperty] = useState<Property | null>(null);

  useEffect(() => {
    if (properties.length > 0) {
      // Center the map on the first property
      setViewState({
        latitude: properties[0].latitude,
        longitude: properties[0].longitude,
        zoom: 11
      });
    }
  }, [properties]);

  return (
    <Map
      {...viewState}
      onMove={evt => setViewState(evt.viewState)}
      style={{width: '100%', height: '400px'}}
      mapStyle="mapbox://styles/mapbox/streets-v11"
      mapboxAccessToken={MAPBOX_TOKEN}
    >
      <FullscreenControl position="top-left" />
      <NavigationControl position="top-left" />
      <GeolocateControl position="top-left" />

      {properties.map((property) => (
        <Marker
          key={property.id}
          latitude={property.latitude}
          longitude={property.longitude}
          onClick={e => {
            e.originalEvent.stopPropagation();
            setSelectedProperty(property);
          }}
          color="#FF0000"
        >
          <svg
            height="20"
            viewBox="0 0 24 24"
            style={{
              cursor: 'pointer',
              fill: '#d00',
              stroke: 'none',
              transform: `translate(${-20 / 2}px,${-20}px)`
            }}
          >
            <path d="M20.2,15.7L20.2,15.7c1.1-1.6,1.8-3.6,1.8-5.7c0-5.6-4.5-10-10-10S2,4.5,2,10c0,2,0.6,3.9,1.6,5.4c0,0.1,0.1,0.2,0.2,0.3
              c0,0,0.1,0.1,0.1,0.2c0.2,0.3,0.4,0.6,0.7,0.9c2.6,3.1,7.4,7.6,7.4,7.6s4.8-4.5,7.4-7.5c0.2-0.3,0.5-0.6,0.7-0.9
              C20.1,15.8,20.2,15.8,20.2,15.7z"/>
          </svg>
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
            <p>Price: ${selectedProperty.price}</p>
            <p>Bedrooms: {selectedProperty.bedrooms}</p>
            <p>Bathrooms: {selectedProperty.bathrooms}</p>
            <p>Square Footage: {selectedProperty.square_footage}</p>
          </div>
        </Popup>
      )}
    </Map>
  );
};

export default PropertyMap;