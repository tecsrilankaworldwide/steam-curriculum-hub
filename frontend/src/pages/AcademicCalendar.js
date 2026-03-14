import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api';
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { Button } from '../components/ui/button';

function AcademicCalendar() {
  const navigate = useNavigate();
  const [lessons, setLessons] = useState([]);
  const [selectedGrade, setSelectedGrade] = useState(1);
  const [selectedTerm, setSelectedTerm] = useState(1);
  const [loading, setLoading] = useState(true);

  useEffect(() => {    loadLessons();
  }, [selectedGrade, selectedTerm]);

  const loadLessons = async () => {
    setLoading(true);
    try {
      const response = await api.getLessons({
        grade: selectedGrade,
        curriculum: 'cambridge'
      });
      
      // Filter by term
      const termLessons = response.data.lessons.filter(
        lesson => lesson.term === selectedTerm
      );
      
      // Sort by week
      termLessons.sort((a, b) => a.week - b.week);
      
      setLessons(termLessons);
    } catch (error) {
      console.error('Error loading lessons:', error);
    } finally {
      setLoading(false);
    }
  };

  const GRADES = ['K', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12];

  return (
    <div className="min-h-screen bg-background">
      <div className="max-w-7xl mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold mb-4">📅 Academic Calendar</h1>
        <p className="text-muted-foreground mb-8">
          3 Terms × 12 Weeks = 36 Lessons | 9 Months Learning + 1 Month Exams
        </p>

        {/* Filters */}
        <div className="flex gap-4 mb-8">
          <div>
            <label className="block text-sm font-medium mb-2">Select Grade</label>
            <select
              className="border rounded px-4 py-2"
              value={selectedGrade}
              onChange={(e) => setSelectedGrade(e.target.value === 'K' ? 'K' : parseInt(e.target.value))}
            >
              {GRADES.map(g => (
                <option key={g} value={g}>Grade {g}</option>
              ))}
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium mb-2">Select Term</label>
            <div className="flex gap-2">
              {[1, 2, 3].map(term => (
                <Button
                  key={term}
                  variant={selectedTerm === term ? 'default' : 'outline'}
                  onClick={() => setSelectedTerm(term)}
                >
                  Term {term}
                </Button>
              ))}
            </div>
          </div>
        </div>

        {/* Term Info */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle>Term {selectedTerm} - {selectedGrade === 'K' ? 'Kindergarten' : `Grade ${selectedGrade}`}</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <p className="text-sm text-muted-foreground">Duration</p>
                <p className="text-lg font-semibold">3 Months (12 Weeks)</p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Lessons</p>
                <p className="text-lg font-semibold">{lessons.length} Weekly Lessons</p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Lesson Duration</p>
                <p className="text-lg font-semibold">
                  {selectedGrade === 'K' || selectedGrade <= 2 ? '20' : 
                   selectedGrade <= 5 ? '35' :
                   selectedGrade <= 8 ? '45' : '55'} minutes
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Weekly Lessons */}
        {loading ? (
          <div className="text-center py-20">Loading calendar...</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {lessons.map(lesson => (
              <Card key={lesson.id} className="hover:shadow-lg transition-shadow">
                <CardHeader>
                  <div className="flex justify-between items-start mb-2">
                    <Badge>Week {lesson.week}</Badge>
                    <Badge variant="outline">{lesson.estimated_duration} min</Badge>
                  </div>
                  <CardTitle className="text-lg">{lesson.title.en}</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground mb-4">
                    {lesson.description.en}
                  </p>
                  <Button
                    size="sm"
                    onClick={() => navigate(`/lesson/${lesson.id}`)}
                    className="w-full"
                  >
                    Start Week {lesson.week} Lesson
                  </Button>
                </CardContent>
              </Card>
            ))}
          </div>
        )}

        {/* Exam Month Info */}
        <Card className="mt-8">
          <CardHeader>
            <CardTitle>📝 Month 10: Exam Schedule</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="border-l-4 border-blue-500 pl-4">
                <p className="font-semibold">Week 1-2</p>
                <p className="text-sm text-muted-foreground">Revision Period</p>
                <p className="text-xs mt-1">Review all Term 1-3 content</p>
              </div>
              <div className="border-l-4 border-green-500 pl-4">
                <p className="font-semibold">Week 3</p>
                <p className="text-sm text-muted-foreground">Free Time</p>
                <p className="text-xs mt-1">Training & preparation</p>
              </div>
              <div className="border-l-4 border-red-500 pl-4">
                <p className="font-semibold">Week 4</p>
                <p className="text-sm text-muted-foreground">Final Exam</p>
                <p className="text-xs mt-1">Assessment week</p>
              </div>
              <div className="border-l-4 border-purple-500 pl-4">
                <p className="font-semibold">After Exam</p>
                <p className="text-sm text-muted-foreground">Certificate</p>
                <p className="text-xs mt-1">Download completion certificate</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

export default AcademicCalendar;
