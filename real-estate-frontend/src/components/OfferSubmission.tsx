import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import './OfferSubmission.css';

interface OfferFormData {
  amount: string;
  name: string;
  phone: string;
  email: string;
}

const OfferSubmissionForm: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const [formData, setFormData] = useState<OfferFormData>({
    amount: '',
    name: '',
    phone: '',
    email: '',
  });

  const [errors, setErrors] = useState<Partial<OfferFormData>>({});

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    // Clear the error when the user starts typing
    if (errors[name as keyof OfferFormData]) {
      setErrors(prev => ({ ...prev, [name]: undefined }));
    }
  };

  const validateForm = (): boolean => {
    const newErrors: Partial<OfferFormData> = {};

    if (!formData.amount || isNaN(Number(formData.amount))) {
      newErrors.amount = 'Please enter a valid amount';
    }
    if (!formData.name.trim()) {
      newErrors.name = 'Name is required';
    }
    if (!formData.phone.trim()) {
      newErrors.phone = 'Phone number is required';
    }
    if (!formData.email.trim() || !formData.email.includes('@')) {
      newErrors.email = 'Please enter a valid email address';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    try {
      const response = await fetch(`http://127.0.0.1:5000/properties/${id}/offers`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}` // Assuming you store the token in localStorage
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        throw new Error('Failed to submit offer');
      }

      // Offer submitted successfully
      alert('Offer submitted successfully!');
      navigate(`/property/${id}`); // Redirect to property details page
    } catch (error) {
      console.error('Error submitting offer:', error);
      alert('Failed to submit offer. Please try again.');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="offer-form">
      <h2>Submit an Offer</h2>
      <div className="form-group">
        <label htmlFor="amount">Offer Amount ($)</label>
        <input
          type="text"
          id="amount"
          name="amount"
          value={formData.amount}
          onChange={handleChange}
          placeholder="Enter offer amount"
        />
        {errors.amount && <span className="error">{errors.amount}</span>}
      </div>
      <div className="form-group">
        <label htmlFor="name">Full Name</label>
        <input
          type="text"
          id="name"
          name="name"
          value={formData.name}
          onChange={handleChange}
          placeholder="Enter your full name"
        />
        {errors.name && <span className="error">{errors.name}</span>}
      </div>
      <div className="form-group">
        <label htmlFor="phone">Phone Number</label>
        <input
          type="tel"
          id="phone"
          name="phone"
          value={formData.phone}
          onChange={handleChange}
          placeholder="Enter your phone number"
        />
        {errors.phone && <span className="error">{errors.phone}</span>}
      </div>
      <div className="form-group">
        <label htmlFor="email">Email Address</label>
        <input
          type="email"
          id="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          placeholder="Enter your email address"
        />
        {errors.email && <span className="error">{errors.email}</span>}
      </div>
      <button type="submit" className="submit-button">Submit Offer</button>
    </form>
  );
};

export default OfferSubmissionForm;