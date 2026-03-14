import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/card';

function InquiryForm() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    organization: '',
    curriculum: 'cambridge',
    grade_range: '',
    num_students: '',
    message: ''
  });
  const [submitted, setSubmitted] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.createInquiry(formData);
      setSubmitted(true);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to submit inquiry');
    }
  };

  if (submitted) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-secondary">
        <Card className="w-full max-w-md text-center">
          <CardContent className="py-8">
            <div className="text-6xl mb-4">✅</div>
            <h2 className="text-2xl font-bold mb-4">Thank You!</h2>
            <p className="text-muted-foreground mb-6">
              We've received your inquiry and will get back to you soon.
            </p>
            <Button onClick={() => navigate('/')}>Back to Home</Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-secondary">
      <Card className="w-full max-w-2xl">
        <CardHeader>
          <CardTitle className="text-2xl">Contact for Pricing</CardTitle>
          <p className="text-muted-foreground">Get custom pricing for your institution</p>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            {error && <div className="text-red-500 text-sm">{error}</div>}
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-1">Name *</label>
                <Input 
                  type="text" 
                  value={formData.name} 
                  onChange={(e) => setFormData({...formData, name: e.target.value})}
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Email *</label>
                <Input 
                  type="email" 
                  value={formData.email} 
                  onChange={(e) => setFormData({...formData, email: e.target.value})}
                  required
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Organization</label>
              <Input 
                type="text" 
                value={formData.organization} 
                onChange={(e) => setFormData({...formData, organization: e.target.value})}
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-1">Curriculum *</label>
                <select 
                  className="w-full border rounded px-3 py-2"
                  value={formData.curriculum}
                  onChange={(e) => setFormData({...formData, curriculum: e.target.value})}
                  required
                >
                  <option value="cambridge">Cambridge</option>
                  <option value="edexcel">Edexcel</option>
                  <option value="asdn">ASDN</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Grade Range *</label>
                <Input 
                  type="text" 
                  placeholder="e.g., 5-8"
                  value={formData.grade_range} 
                  onChange={(e) => setFormData({...formData, grade_range: e.target.value})}
                  required
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Number of Students</label>
              <Input 
                type="number" 
                value={formData.num_students} 
                onChange={(e) => setFormData({...formData, num_students: e.target.value})}
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Message *</label>
              <textarea 
                className="w-full border rounded px-3 py-2 min-h-[100px]"
                value={formData.message} 
                onChange={(e) => setFormData({...formData, message: e.target.value})}
                required
              />
            </div>

            <div className="flex gap-4">
              <Button type="submit" className="flex-1">
                Submit Inquiry
              </Button>
              <Button type="button" variant="outline" onClick={() => navigate('/')}>
                Cancel
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}

export default InquiryForm;
