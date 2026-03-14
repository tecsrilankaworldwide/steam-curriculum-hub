import React, { useState, useEffect } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { toast } from '../components/ui/sonner';
import { CheckCircle2, Loader2, XCircle } from 'lucide-react';
import api from '../api';

const PaymentSuccess = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const [status, setStatus] = useState('checking'); // checking, success, failed
  const [paymentData, setPaymentData] = useState(null);
  const sessionId = searchParams.get('session_id');

  useEffect(() => {
    if (sessionId) {
      pollPaymentStatus(sessionId, 0);
    } else {
      setStatus('failed');
    }
  }, [sessionId]);

  const pollPaymentStatus = async (sid, attempts) => {
    const maxAttempts = 5;
    const pollInterval = 2000;

    if (attempts >= maxAttempts) {
      setStatus('failed');
      toast.error('Payment status check timed out. Please contact support.');
      return;
    }

    try {
      const response = await api.getCheckoutStatus(sid);
      const data = response.data;
      setPaymentData(data);

      if (data.payment_status === 'paid') {
        setStatus('success');
        toast.success('Payment successful! Welcome to your plan.');
        return;
      } else if (data.status === 'expired') {
        setStatus('failed');
        toast.error('Payment session expired. Please try again.');
        return;
      }

      // Continue polling
      setTimeout(() => pollPaymentStatus(sid, attempts + 1), pollInterval);
    } catch (error) {
      console.error('Error checking payment status:', error);
      if (attempts < maxAttempts - 1) {
        setTimeout(() => pollPaymentStatus(sid, attempts + 1), pollInterval);
      } else {
        setStatus('failed');
      }
    }
  };

  return (
    <div className="min-h-screen bg-background flex items-center justify-center p-4" data-testid="payment-success-page">
      <Card className="max-w-md w-full">
        <CardHeader className="text-center">
          {status === 'checking' && (
            <>
              <Loader2 className="w-16 h-16 text-primary mx-auto mb-4 animate-spin" />
              <CardTitle data-testid="payment-status-title">Processing Payment...</CardTitle>
            </>
          )}
          {status === 'success' && (
            <>
              <CheckCircle2 className="w-16 h-16 text-primary mx-auto mb-4" />
              <CardTitle data-testid="payment-status-title">Payment Successful!</CardTitle>
            </>
          )}
          {status === 'failed' && (
            <>
              <XCircle className="w-16 h-16 text-destructive mx-auto mb-4" />
              <CardTitle data-testid="payment-status-title">Payment Issue</CardTitle>
            </>
          )}
        </CardHeader>
        <CardContent className="text-center space-y-4">
          {status === 'checking' && (
            <p className="text-muted-foreground">Please wait while we confirm your payment...</p>
          )}
          {status === 'success' && (
            <>
              <p className="text-muted-foreground">
                Your subscription is now active. Enjoy unlimited access to all lessons!
              </p>
              {paymentData && (
                <div className="bg-muted p-4 rounded-lg text-sm">
                  <p>Amount: ${(paymentData.amount_total / 100).toFixed(2)} {paymentData.currency?.toUpperCase()}</p>
                </div>
              )}
              <Button onClick={() => navigate('/lessons')} className="w-full" data-testid="go-to-lessons-btn">
                Start Learning
              </Button>
            </>
          )}
          {status === 'failed' && (
            <>
              <p className="text-muted-foreground">
                There was an issue with your payment. Please try again or contact support.
              </p>
              <div className="flex gap-2">
                <Button onClick={() => navigate('/pricing')} className="flex-1" data-testid="try-again-btn">
                  Try Again
                </Button>
                <Button onClick={() => navigate('/')} variant="outline" className="flex-1">
                  Go Home
                </Button>
              </div>
            </>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default PaymentSuccess;
