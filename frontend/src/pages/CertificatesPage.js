import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import api from '../api';
import { Button } from '../components/ui/button';
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { Award, Lock, Unlock, CheckCircle, Clock } from 'lucide-react';
import { toast } from '../components/ui/sonner';

const AGE_GROUP_INFO = {
  '5-7': {
    title: 'Little Explorers',
    subtitle: 'Kindergarten to Grade 2',
    icon: '🌱',
    color: 'emerald',
    bgColor: 'bg-emerald-50',
    borderColor: 'border-emerald-400'
  },
  '8-9': {
    title: 'Young Thinkers',
    subtitle: 'Grade 3 to Grade 4',
    icon: '🔬',
    color: 'sky',
    bgColor: 'bg-sky-50',
    borderColor: 'border-sky-400'
  },
  '10-12': {
    title: 'Junior Scientists',
    subtitle: 'Grade 5 to Grade 7',
    icon: '🧪',
    color: 'violet',
    bgColor: 'bg-violet-50',
    borderColor: 'border-violet-400'
  },
  '13-15': {
    title: 'Tech Innovators',
    subtitle: 'Grade 8 to Grade 10',
    icon: '💡',
    color: 'amber',
    bgColor: 'bg-amber-50',
    borderColor: 'border-amber-400'
  },
  '16-18': {
    title: 'Future Leaders',
    subtitle: 'Grade 11 to Grade 12',
    icon: '🎓',
    color: 'rose',
    bgColor: 'bg-rose-50',
    borderColor: 'border-rose-400'
  }
};

function CertificatesPage() {
  const navigate = useNavigate();
  const { t } = useTranslation();
  const [progress, setProgress] = useState([]);
  const [loading, setLoading] = useState(true);
  const [requesting, setRequesting] = useState(null);

  useEffect(() => {
    loadProgress();
  }, []);

  const loadProgress = async () => {
    try {
      setLoading(true);
      const response = await api.get('/certificates/progress');
      setProgress(response.data.progress);
    } catch (error) {
      console.error('Error loading progress:', error);
      if (error.response?.status === 401) {
        toast.error('Please login to view certificates');
        navigate('/login');
      }
    } finally {
      setLoading(false);
    }
  };

  const requestCertificate = async (ageGroup) => {
    try {
      setRequesting(ageGroup);
      const response = await api.post('/certificates/request', null, {
        params: { age_group: ageGroup }
      });
      toast.success('Certificate approved! 🎉');
      loadProgress(); // Reload to show certificate
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Error requesting certificate');
    } finally {
      setRequesting(null);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p>Loading certificates...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      <div className="max-w-6xl mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2">Your Certificates</h1>
          <p className="text-muted-foreground">
            Complete lessons to unlock certificates for each age group
          </p>
        </div>

        <div className="grid gap-6">
          {progress.map((item) => {
            const info = AGE_GROUP_INFO[item.age_group];
            const progressPct = item.progress_percentage;
            const isUnlocked = item.unlocked;
            const hasCertificate = item.certificate_number;

            return (
              <Card
                key={item.age_group}
                className={`${info.bgColor} border-2 ${info.borderColor} transition-all hover:shadow-lg`}
              >
                <CardContent className="p-6">
                  <div className="flex items-start gap-6">
                    {/* Icon */}
                    <div className="flex-shrink-0">
                      <div className="w-20 h-20 rounded-full bg-white flex items-center justify-center text-4xl shadow-md">
                        {info.icon}
                      </div>
                    </div>

                    {/* Info */}
                    <div className="flex-1">
                      <div className="flex items-start justify-between mb-4">
                        <div>
                          <h3 className="text-2xl font-bold mb-1">{info.title}</h3>
                          <p className="text-sm text-muted-foreground">
                            {info.subtitle} • Ages {item.age_group}
                          </p>
                        </div>
                        {hasCertificate ? (
                          <Badge className="bg-green-600 text-white">
                            <CheckCircle className="w-4 h-4 mr-1" />
                            Certified
                          </Badge>
                        ) : isUnlocked ? (
                          <Badge className="bg-blue-600 text-white">
                            <Unlock className="w-4 h-4 mr-1" />
                            Ready
                          </Badge>
                        ) : (
                          <Badge variant="secondary">
                            <Lock className="w-4 h-4 mr-1" />
                            Locked
                          </Badge>
                        )}
                      </div>

                      {/* Progress Bar */}
                      <div className="mb-4">
                        <div className="flex items-center justify-between mb-2">
                          <span className="text-sm font-medium">
                            Progress: {item.completed_lessons}/{item.total_lessons} lessons
                          </span>
                          <span className="text-sm font-medium">
                            {progressPct.toFixed(0)}%
                          </span>
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
                          <div
                            className={`h-full bg-${info.color}-500 transition-all duration-500`}
                            style={{ width: `${progressPct}%` }}
                          />
                        </div>
                        {!isUnlocked && (
                          <p className="text-xs text-muted-foreground mt-2">
                            Complete 80% of lessons to unlock certificate
                          </p>
                        )}
                      </div>

                      {/* Actions */}
                      <div className="flex gap-3">
                        {hasCertificate ? (
                          <>
                            <Button
                              onClick={() => navigate(`/certificate/${item.certificate_number}`)}
                              className="bg-green-600 hover:bg-green-700"
                            >
                              <Award className="w-4 h-4 mr-2" />
                              View Certificate
                            </Button>
                            <Button
                              variant="outline"
                              onClick={() => window.open(`/certificate/${item.certificate_number}`, '_blank')}
                            >
                              Print / Download
                            </Button>
                          </>
                        ) : isUnlocked ? (
                          <Button
                            onClick={() => requestCertificate(item.age_group)}
                            disabled={requesting === item.age_group}
                            className="bg-blue-600 hover:bg-blue-700"
                          >
                            {requesting === item.age_group ? (
                              <>
                                <Clock className="w-4 h-4 mr-2 animate-spin" />
                                Requesting...
                              </>
                            ) : (
                              <>
                                <Award className="w-4 h-4 mr-2" />
                                Request Certificate
                              </>
                            )}
                          </Button>
                        ) : (
                          <Button
                            onClick={() => navigate(`/lessons?age_group=${item.age_group}`)}
                            variant="outline"
                          >
                            Continue Learning
                          </Button>
                        )}
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>
      </div>
    </div>
  );
}

export default CertificatesPage;
