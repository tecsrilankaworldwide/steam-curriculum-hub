import React, { useState, useEffect } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Badge } from '../components/ui/badge';
import { toast } from '../components/ui/sonner';
import { Check, Copy, QrCode, CreditCard, Loader2, CheckCircle2, XCircle } from 'lucide-react';
import api from '../api';

const PricingPage = () => {
  const [showQRCode, setShowQRCode] = useState(false);
  const [selectedPlan, setSelectedPlan] = useState(null);
  const [loading, setLoading] = useState(false);
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();

  const plans = [
    {
      id: 'free',
      name: 'Free Tier',
      price: 0,
      currency: 'USD',
      features: [
        '10 lessons per month',
        'View lesson previews',
        'Basic progress tracking',
        'Community features'
      ]
    },
    {
      id: 'standard',
      name: 'Standard',
      price: 5,
      priceInLKR: 1500,
      currency: 'USD',
      popular: true,
      features: [
        'Unlimited access to 1,050 AI lessons',
        'Download lessons as PDF',
        'All languages supported',
        'Quiz system',
        'Progress tracking',
        'Word glossary'
      ]
    },
    {
      id: 'premium',
      name: 'Premium',
      price: 10,
      priceInLKR: 3000,
      currency: 'USD',
      features: [
        'Everything in Standard',
        'Certificate generation',
        'Priority support',
        'Early access to new content',
        'Ad-free experience',
        'Offline downloads'
      ]
    }
  ];

  const handleSubscribe = async (plan) => {
    if (plan.id === 'free') {
      toast.success('Welcome to Free Tier! Start exploring lessons.');
      navigate('/lessons');
      return;
    }
    
    setSelectedPlan(plan);
    setShowQRCode(true);
  };

  const handleStripeCheckout = async (plan) => {
    setLoading(true);
    try {
      const originUrl = window.location.origin;
      const response = await api.createCheckoutSession({
        package_id: plan.id,
        origin_url: originUrl,
      });
      
      if (response.data.url) {
        window.location.href = response.data.url;
      } else {
        toast.error('Failed to create checkout session');
      }
    } catch (error) {
      console.error('Stripe checkout error:', error);
      toast.error('Payment error. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleCopyUPI = () => {
    navigator.clipboard.writeText('payments@steamhub.edu');
    toast.success('Payment ID copied to clipboard!');
  };

  return (
    <div className="min-h-screen bg-background py-12 px-4" data-testid="pricing-page">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl sm:text-5xl font-semibold tracking-tight mb-4" data-testid="pricing-title">
            Choose Your Learning Plan
          </h1>
          <p className="text-lg text-muted-foreground">
            Access world-class AI education for children ages 5-18
          </p>
          <p className="text-base text-primary font-semibold mt-2">
            Special Payment Options for Sri Lanka Available!
          </p>
        </div>

        {/* Pricing Cards */}
        <div className="grid md:grid-cols-3 gap-8 mb-12">
          {plans.map((plan) => (
            <Card 
              key={plan.id}
              className={`relative transition-all duration-200 hover:shadow-lg ${plan.popular ? 'border-2 border-primary shadow-xl ring-1 ring-primary/20' : 'border hover:border-primary/40'}`}
              data-testid={`pricing-card-${plan.id}`}
            >
              {plan.popular && (
                <div className="absolute -top-3 left-1/2 transform -translate-x-1/2">
                  <Badge className="bg-primary text-primary-foreground px-4 py-1">
                    MOST POPULAR
                  </Badge>
                </div>
              )}
              
              <CardHeader className="pt-8">
                <CardTitle className="text-2xl">{plan.name}</CardTitle>
                <div className="mt-4">
                  <span className="text-5xl font-bold text-primary">
                    ${plan.price}
                  </span>
                  <span className="text-muted-foreground">/month</span>
                  
                  {plan.priceInLKR && (
                    <div className="mt-2 text-lg text-muted-foreground font-semibold">
                      LKR {plan.priceInLKR}/month
                    </div>
                  )}
                </div>
              </CardHeader>

              <CardContent>
                <ul className="space-y-3 mb-6">
                  {plan.features.map((feature, idx) => (
                    <li key={idx} className="flex items-start gap-2">
                      <Check className="w-5 h-5 text-primary flex-shrink-0 mt-0.5" />
                      <span className="text-sm">{feature}</span>
                    </li>
                  ))}
                </ul>

                <Button
                  onClick={() => handleSubscribe(plan)}
                  className="w-full"
                  variant={plan.id === 'free' ? 'outline' : 'default'}
                  data-testid={`subscribe-${plan.id}-btn`}
                >
                  {plan.id === 'free' ? 'Get Started Free' : 'Subscribe Now'}
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Payment Modal */}
        {showQRCode && selectedPlan && (
          <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4" data-testid="payment-modal">
            <Card className="max-w-2xl w-full max-h-[90vh] overflow-y-auto">
              <CardHeader>
                <CardTitle className="text-2xl flex items-center gap-2">
                  <CreditCard className="w-6 h-6" />
                  Payment — {selectedPlan.name} (${selectedPlan.price}/mo)
                </CardTitle>
              </CardHeader>

              <CardContent>
                <div className="grid md:grid-cols-2 gap-8">
                  {/* Stripe Payment */}
                  <div>
                    <h3 className="text-xl font-bold mb-4 text-primary">
                      International Payment
                    </h3>
                    <p className="mb-4 text-muted-foreground">Pay via Stripe (Credit/Debit Card)</p>
                    <p className="text-3xl font-bold mb-4">${selectedPlan.price}/month</p>
                    <Button 
                      className="w-full"
                      onClick={() => handleStripeCheckout(selectedPlan)}
                      disabled={loading}
                      data-testid="stripe-pay-btn"
                    >
                      {loading ? (
                        <>
                          <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                          Redirecting to Stripe...
                        </>
                      ) : (
                        <>
                          <CreditCard className="w-4 h-4 mr-2" />
                          Pay with Stripe
                        </>
                      )}
                    </Button>
                  </div>

                  {/* Sri Lanka QR Payment */}
                  <div className="md:border-l md:pl-8">
                    <h3 className="text-xl font-bold mb-4 text-primary">
                      Sri Lanka Payment
                    </h3>
                    <p className="mb-2 text-muted-foreground">Bank Transfer / QR Code</p>
                    <p className="text-3xl font-bold mb-4">LKR {selectedPlan.priceInLKR}</p>
                    
                    <div className="bg-muted p-4 rounded-lg mb-4">
                      <p className="text-sm mb-2">
                        <strong>Bank Transfer Details:</strong>
                      </p>
                      <div className="flex items-center gap-2">
                        <code className="bg-background px-2 py-1 rounded text-sm flex-1 font-mono">
                          payments@steamhub.edu
                        </code>
                        <Button 
                          size="sm" 
                          variant="outline"
                          onClick={handleCopyUPI}
                          data-testid="copy-payment-id-btn"
                        >
                          <Copy className="w-4 h-4" />
                        </Button>
                      </div>
                    </div>

                    <p className="text-xs text-muted-foreground mb-4">
                      After payment, send screenshot to support@steamhub.edu for activation
                    </p>

                    <Button 
                      className="w-full"
                      variant="outline"
                      onClick={() => {
                        toast.success('Payment confirmation noted! Check your email for activation.');
                        setShowQRCode(false);
                      }}
                      data-testid="payment-done-btn"
                    >
                      I've Completed Payment
                    </Button>
                  </div>
                </div>

                <Button
                  className="w-full mt-6"
                  variant="ghost"
                  onClick={() => setShowQRCode(false)}
                  data-testid="payment-cancel-btn"
                >
                  Cancel
                </Button>
              </CardContent>
            </Card>
          </div>
        )}

        {/* Features Grid */}
        <div className="mt-16">
          <h2 className="text-3xl font-semibold text-center mb-8">
            Why Choose STEAM Curriculum Hub?
          </h2>
          
          <div className="grid md:grid-cols-4 gap-6">
            {[
              { icon: '1,050+', title: 'AI Lessons', desc: 'Comprehensive curriculum from basics to advanced' },
              { icon: '9+', title: 'Languages', desc: 'Learn in Sinhala, Tamil, Hindi, Chinese & more' },
              { icon: '5-18', title: 'Ages', desc: 'Perfect progression from kindergarten to college prep' },
              { icon: 'PDF', title: 'Download & Share', desc: 'Access offline and share with friends' },
            ].map((item, idx) => (
              <Card key={idx}>
                <CardContent className="pt-6 text-center">
                  <div className="text-3xl font-bold text-primary mb-2">{item.icon}</div>
                  <h3 className="font-bold mb-2">{item.title}</h3>
                  <p className="text-sm text-muted-foreground">{item.desc}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default PricingPage;
