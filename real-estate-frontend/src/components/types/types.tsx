export interface Property {
    id: number;
    address: string;
    price: number;
    bedrooms: number;
    bathrooms: number;
    square_footage: number;
    latitude: number;
    longitude: number;
    image_urls: string[] | null;
    offer: any;
  }