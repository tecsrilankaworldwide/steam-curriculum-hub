import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import api from '../api';
import { Button } from '../components/ui/button';
import { Download, Share2, CheckCircle } from 'lucide-react';

function CertificatePage() {
  const { certNumber } = useParams();
  const [certificate, setCertificate] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadCertificate();
  }, [certNumber]);

  const loadCertificate = async () => {
    try {
      const response = await api.get(`/certificates/${certNumber}`);
      setCertificate(response.data);
    } catch (error) {
      console.error('Error loading certificate:', error);
    } finally {
      setLoading(false);
    }
  };

  const handlePrint = () => {
    window.print();
  };

  if (loading) {
    return <div className="flex items-center justify-center min-h-screen">Loading...</div>;
  }

  if (!certificate) {
    return <div className="flex items-center justify-center min-h-screen">Certificate not found</div>;
  }

  const ageGroupNames = {
    '5-7': 'Little Explorers (Ages 5-7)',
    '8-9': 'Young Thinkers (Ages 8-9)',
    '10-12': 'Junior Scientists (Ages 10-12)',
    '13-15': 'Tech Innovators (Ages 13-15)',
    '16-18': 'Future Leaders (Ages 16-18)'
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Print Button - Hidden when printing */}
      <div className="print:hidden bg-white border-b sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-xl font-bold">Certificate Preview</h1>
          <div className="flex gap-2">
            <Button onClick={handlePrint} className="bg-blue-600 hover:bg-blue-700">
              <Download className="w-4 h-4 mr-2" />
              Print / Save PDF
            </Button>
          </div>
        </div>
      </div>

      {/* Certificate Design */}
      <div className="py-8 print:py-0">
        <div className="max-w-4xl mx-auto">
          <div 
            className="bg-white p-12 print:p-16 shadow-xl print:shadow-none"
            style={{
              border: '8px solid #0891B2',
              borderRadius: '8px',
              minHeight: '11in',
              position: 'relative'
            }}
          >
            {/* Header */}
            <div className="text-center mb-8">
              <div className="text-5xl font-bold text-cyan-600 mb-2">CERTIFICATE</div>
              <div className="text-2xl font-semibold text-gray-700">of Completion</div>
              <div className="w-32 h-1 bg-cyan-600 mx-auto mt-4"></div>
            </div>

            {/* Body */}
            <div className="text-center mb-8">
              <p className="text-lg text-gray-600 mb-4">This is to certify that</p>
              
              <div className="text-4xl font-bold text-cyan-700 mb-6 py-2">
                {certificate.student_name}
              </div>

              <p className="text-lg text-gray-600 mb-4">has successfully completed</p>
              
              <div className="text-3xl font-bold text-gray-800 mb-2">
                {ageGroupNames[certificate.age_group]}
              </div>
              
              <div className="text-xl text-gray-700 mb-6">
                {certificate.program}
              </div>

              <div className="flex justify-center gap-8 mb-8">
                <div className="text-center">
                  <div className="text-3xl font-bold text-cyan-600">{certificate.completed_lessons}</div>
                  <div className="text-sm text-gray-600">Lessons Completed</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-cyan-600">
                    {Math.round(certificate.completed_lessons / certificate.total_lessons * 100)}%
                  </div>
                  <div className="text-sm text-gray-600">Achievement</div>
                </div>
              </div>
            </div>

            {/* QR Code & Certificate Number */}
            <div className="flex justify-between items-end mt-12">
              <div className="text-left">
                <p className="text-sm text-gray-600 mb-1">Certificate Number:</p>
                <p className="text-lg font-mono font-bold text-cyan-700">{certificate.certificate_number}</p>
                <p className="text-xs text-gray-500 mt-2">
                  Issued: {new Date(certificate.approved_date).toLocaleDateString()}
                </p>
              </div>

              {certificate.qr_code && (
                <div className="text-center">
                  <img 
                    src={certificate.qr_code} 
                    alt="Verification QR Code" 
                    className="w-24 h-24 mb-1"
                  />
                  <p className="text-xs text-gray-600">Scan to Verify</p>
                </div>
              )}
            </div>

            {/* Signatures */}
            <div className="grid grid-cols-2 gap-12 mt-16">
              <div className="text-center">
                <div className="border-t-2 border-gray-400 pt-2">
                  <p className="font-semibold text-gray-800">Director of Education</p>
                  <p className="text-sm text-gray-600">TEC WORLDWIDE INC.</p>
                </div>
              </div>
              <div className="text-center">
                <div className="border-t-2 border-gray-400 pt-2">
                  <p className="font-semibold text-gray-800">Quality Assurance</p>
                  <p className="text-sm text-gray-600">TEC WORLDWIDE INC.</p>
                </div>
              </div>
            </div>

            {/* Footer */}
            <div className="text-center mt-12 pt-8 border-t border-gray-300">
              <p className="text-sm text-gray-600">Global STEAM Education Hub</p>
              <p className="text-xs text-gray-500">TEC Sri Lanka Worldwide • Empowering Young Minds with AI Education</p>
            </div>

            {/* Watermark */}
            <div 
              className="absolute inset-0 flex items-center justify-center pointer-events-none"
              style={{ opacity: 0.03, zIndex: 0 }}
            >
              <div className="text-9xl font-bold transform rotate-[-45deg]">STEAM</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default CertificatePage;
