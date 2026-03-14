import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import api from '../api';
import { CheckCircle, XCircle, AlertCircle } from 'lucide-react';
import { Card, CardContent } from '../components/ui/card';

function VerifyCertificatePage() {
  const { certNumber } = useParams();
  const [verification, setVerification] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    verifyCertificate();
  }, [certNumber]);

  const verifyCertificate = async () => {
    try {
      const response = await api.get(`/verify/${certNumber}`);
      setVerification(response.data);
    } catch (error) {
      console.error('Error verifying certificate:', error);
      setVerification({ valid: false, message: 'Error verifying certificate' });
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-cyan-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Verifying certificate...</p>
        </div>
      </div>
    );
  }

  const isValid = verification?.valid;

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-3xl mx-auto px-4">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold mb-2">Certificate Verification</h1>
          <p className="text-gray-600">Public verification system for AI & STEAM certificates</p>
        </div>

        {/* Verification Result */}
        <Card className={`border-4 ${
          isValid ? 'border-green-500 bg-green-50' : 'border-red-500 bg-red-50'
        }`}>
          <CardContent className="p-8">
            <div className="text-center mb-6">
              {isValid ? (
                <>
                  <CheckCircle className="w-20 h-20 text-green-600 mx-auto mb-4" />
                  <h2 className="text-3xl font-bold text-green-700 mb-2">
                    Valid Certificate
                  </h2>
                  <p className="text-green-600">{verification.message}</p>
                </>
              ) : (
                <>
                  <XCircle className="w-20 h-20 text-red-600 mx-auto mb-4" />
                  <h2 className="text-3xl font-bold text-red-700 mb-2">
                    Invalid Certificate
                  </h2>
                  <p className="text-red-600">{verification.message}</p>
                </>
              )}
            </div>

            {isValid && verification.certificate && (
              <div className="bg-white rounded-lg p-6 shadow-sm">
                <h3 className="text-xl font-bold mb-4 text-gray-800">Certificate Details</h3>
                
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <p className="text-sm text-gray-600">Certificate Number</p>
                    <p className="font-mono font-bold text-cyan-700">
                      {verification.certificate.certificate_number}
                    </p>
                  </div>
                  
                  <div>
                    <p className="text-sm text-gray-600">Student Name</p>
                    <p className="font-semibold">{verification.certificate.student_name}</p>
                  </div>
                  
                  <div>
                    <p className="text-sm text-gray-600">Program</p>
                    <p className="font-semibold">{verification.certificate.program}</p>
                  </div>
                  
                  <div>
                    <p className="text-sm text-gray-600">Age Group</p>
                    <p className="font-semibold">Ages {verification.certificate.age_group}</p>
                  </div>
                  
                  <div>
                    <p className="text-sm text-gray-600">Lessons Completed</p>
                    <p className="font-semibold">
                      {verification.certificate.completed_lessons} / {verification.certificate.total_lessons}
                    </p>
                  </div>
                  
                  <div>
                    <p className="text-sm text-gray-600">Issued Date</p>
                    <p className="font-semibold">
                      {new Date(verification.certificate.approved_date).toLocaleDateString()}
                    </p>
                  </div>
                </div>

                <div className="mt-6 p-4 bg-green-100 rounded-lg">
                  <div className="flex items-start gap-3">
                    <CheckCircle className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
                    <div>
                      <p className="font-semibold text-green-800 mb-1">Verified Authentic</p>
                      <p className="text-sm text-green-700">
                        This certificate has been verified as authentic and was issued by 
                        TEC Sri Lanka Worldwide through the Global STEAM Education Hub.
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {!isValid && (
              <div className="bg-white rounded-lg p-6 shadow-sm">
                <div className="flex items-start gap-3">
                  <AlertCircle className="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" />
                  <div>
                    <p className="font-semibold text-gray-800 mb-2">Certificate Not Found</p>
                    <p className="text-sm text-gray-600">
                      The certificate number <span className="font-mono font-bold">{certNumber}</span> could not be found in our system. 
                      Please verify the certificate number and try again.
                    </p>
                  </div>
                </div>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Footer Info */}
        <div className="mt-8 text-center text-sm text-gray-600">
          <p>For questions about this certificate, please contact:</p>
          <p className="font-semibold mt-1">TEC Sri Lanka Worldwide</p>
          <p>Global STEAM Education Hub</p>
        </div>
      </div>
    </div>
  );
}

export default VerifyCertificatePage;
