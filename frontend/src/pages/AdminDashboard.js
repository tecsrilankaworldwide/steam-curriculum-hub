import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { toast } from '../components/ui/sonner';

function useAuth() {
  const user = JSON.parse(localStorage.getItem('user') || 'null');
  return { user };
}

// Grade options for K-12
const GRADE_OPTIONS = ['K', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12];
const CURRICULUM_OPTIONS = ['cambridge', 'edexcel', 'asdn'];
const SUBJECT_OPTIONS = ['mathematics', 'physics', 'chemistry', 'biology', 'science', 'technology', 'engineering', 'arts', 'english', 'ict'];
const DIFFICULTY_OPTIONS = ['easy', 'medium', 'hard'];

function LessonForm({ lesson, onSave, onCancel }) {
  const [formData, setFormData] = useState(lesson || {
    title: { en: '', local: '' },
    description: { en: '', local: '' },
    content: { en: '', local: '' },
    curriculum: 'cambridge',
    subject: 'mathematics',
    grade: 5,
    language_code: 'hi-IN',
    difficulty: 'medium',
    estimated_duration: 30,
    source: 'OpenStax',
    license: 'CC BY 4.0',
    source_url: 'https://openstax.org'
  });
  
  const [saving, setSaving] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    try {
      await onSave(formData);
    } catch (error) {
      toast.error('Error saving lesson: ' + error.message);
    } finally {
      setSaving(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium mb-1">Title (English) *</label>
          <Input
            value={formData.title.en}
            onChange={(e) => setFormData({...formData, title: {...formData.title, en: e.target.value}})}
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Title (Local) *</label>
          <Input
            value={formData.title.local}
            onChange={(e) => setFormData({...formData, title: {...formData.title, local: e.target.value}})}
            required
          />
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium mb-1">Description (English) *</label>
          <textarea
            className="w-full border rounded px-3 py-2"
            rows="3"
            value={formData.description.en}
            onChange={(e) => setFormData({...formData, description: {...formData.description, en: e.target.value}})}
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Description (Local) *</label>
          <textarea
            className="w-full border rounded px-3 py-2"
            rows="3"
            value={formData.description.local}
            onChange={(e) => setFormData({...formData, description: {...formData.description, local: e.target.value}})}
            required
          />
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium mb-1">Content (English) *</label>
          <textarea
            className="w-full border rounded px-3 py-2"
            rows="5"
            value={formData.content.en}
            onChange={(e) => setFormData({...formData, content: {...formData.content, en: e.target.value}})}
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Content (Local) *</label>
          <textarea
            className="w-full border rounded px-3 py-2"
            rows="5"
            value={formData.content.local}
            onChange={(e) => setFormData({...formData, content: {...formData.content, local: e.target.value}})}
            required
          />
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div>
          <label className="block text-sm font-medium mb-1">Curriculum *</label>
          <select
            className="w-full border rounded px-3 py-2"
            value={formData.curriculum}
            onChange={(e) => setFormData({...formData, curriculum: e.target.value})}
            required
          >
            {CURRICULUM_OPTIONS.map(c => (
              <option key={c} value={c}>{c.toUpperCase()}</option>
            ))}
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Subject *</label>
          <select
            className="w-full border rounded px-3 py-2"
            value={formData.subject}
            onChange={(e) => setFormData({...formData, subject: e.target.value})}
            required
          >
            {SUBJECT_OPTIONS.map(s => (
              <option key={s} value={s}>{s.charAt(0).toUpperCase() + s.slice(1)}</option>
            ))}
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Grade *</label>
          <select
            className="w-full border rounded px-3 py-2"
            value={formData.grade}
            onChange={(e) => setFormData({...formData, grade: e.target.value === 'K' ? 'K' : parseInt(e.target.value)})}
            required
          >
            {GRADE_OPTIONS.map(g => (
              <option key={g} value={g}>Grade {g}</option>
            ))}
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Difficulty *</label>
          <select
            className="w-full border rounded px-3 py-2"
            value={formData.difficulty}
            onChange={(e) => setFormData({...formData, difficulty: e.target.value})}
            required
          >
            {DIFFICULTY_OPTIONS.map(d => (
              <option key={d} value={d}>{d.charAt(0).toUpperCase() + d.slice(1)}</option>
            ))}
          </select>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <label className="block text-sm font-medium mb-1">Duration (minutes) *</label>
          <Input
            type="number"
            value={formData.estimated_duration}
            onChange={(e) => setFormData({...formData, estimated_duration: parseInt(e.target.value)})}
            required
            min="1"
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Source *</label>
          <Input
            value={formData.source}
            onChange={(e) => setFormData({...formData, source: e.target.value})}
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">License *</label>
          <select
            className="w-full border rounded px-3 py-2"
            value={formData.license}
            onChange={(e) => setFormData({...formData, license: e.target.value})}
            required
          >
            <option value="CC BY 4.0">CC BY 4.0</option>
            <option value="CC BY-NC 3.0">CC BY-NC 3.0</option>
            <option value="CC BY-SA 4.0">CC BY-SA 4.0</option>
          </select>
        </div>
      </div>

      <div>
        <label className="block text-sm font-medium mb-1">Source URL</label>
        <Input
          type="url"
          value={formData.source_url || ''}
          onChange={(e) => setFormData({...formData, source_url: e.target.value})}
        />
      </div>

      <div className="flex gap-4">
        <Button type="submit" disabled={saving}>
          {saving ? 'Saving...' : lesson ? 'Update Lesson' : 'Create Lesson'}
        </Button>
        <Button type="button" variant="outline" onClick={onCancel}>
          Cancel
        </Button>
      </div>
    </form>
  );
}

function AdminDashboard() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('inquiries');
  const [inquiries, setInquiries] = useState([]);
  const [lessons, setLessons] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showLessonForm, setShowLessonForm] = useState(false);
  const [editingLesson, setEditingLesson] = useState(null);

  useEffect(() => {
    if (!user || user.role !== 'admin') {
      navigate('/login');
      return;
    }
    loadData();
  }, [activeTab]);

  const loadData = async () => {
    setLoading(true);
    try {
      if (activeTab === 'inquiries') {
        const response = await api.getInquiries();
        setInquiries(response.data.inquiries);
      } else if (activeTab === 'lessons') {
        const response = await api.getLessons({});
        setLessons(response.data.lessons);
      }
    } catch (error) {
      console.error('Error loading data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateInquiryStatus = async (inquiryId, newStatus) => {
    try {
      await api.updateInquiry(inquiryId, { status: newStatus });
      
      // Send notification (console log for now)
      console.log(`📧 Email Notification: Inquiry ${inquiryId} status updated to ${newStatus}`);
      toast.success(`Inquiry status updated to ${newStatus}. Email notification sent!`);
      
      loadData();
    } catch (error) {
      console.error('Error updating inquiry:', error);
      toast.error('Error updating inquiry');
    }
  };

  const handleDeleteLesson = async (lessonId) => {
    if (window.confirm('Are you sure you want to delete this lesson?')) {
      try {
        await api.deleteLesson(lessonId);
        loadData();
      } catch (error) {
        console.error('Error deleting lesson:', error);
      }
    }
  };

  const handleSaveLesson = async (lessonData) => {
    try {
      if (editingLesson) {
        await api.updateLesson(editingLesson.id, lessonData);
        toast.success('Lesson updated successfully!');
      } else {
        await api.createLesson(lessonData);
        toast.success('Lesson created successfully!');
      }
      setShowLessonForm(false);
      setEditingLesson(null);
      loadData();
    } catch (error) {
      throw error;
    }
  };

  const handleEditLesson = (lesson) => {
    setEditingLesson(lesson);
    setShowLessonForm(true);
  };

  const handleCreateNew = () => {
    setEditingLesson(null);
    setShowLessonForm(true);
  };

  return (
    <div className="min-h-screen bg-background">
      <div className="max-w-7xl mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold mb-8">Admin Dashboard</h1>

        <div className="flex gap-4 mb-8">
          <Button 
            variant={activeTab === 'inquiries' ? 'default' : 'outline'}
            onClick={() => { setActiveTab('inquiries'); setShowLessonForm(false); }}
          >
            Inquiries
          </Button>
          <Button 
            variant={activeTab === 'lessons' ? 'default' : 'outline'}
            onClick={() => { setActiveTab('lessons'); setShowLessonForm(false); }}
          >
            Lessons
          </Button>
        </div>

        {loading ? (
          <div className="text-center py-20">Loading...</div>
        ) : activeTab === 'inquiries' ? (
          <div className="space-y-4">
            <h2 className="text-2xl font-semibold mb-4">Pricing Inquiries ({inquiries.length})</h2>
            {inquiries.length === 0 ? (
              <Card>
                <CardContent className="py-8 text-center text-muted-foreground">
                  No inquiries yet
                </CardContent>
              </Card>
            ) : (
              inquiries.map(inquiry => (
                <Card key={inquiry.id}>
                  <CardHeader>
                    <div className="flex justify-between items-start">
                      <div>
                        <CardTitle>{inquiry.name}</CardTitle>
                        <p className="text-sm text-muted-foreground mt-1">{inquiry.email}</p>
                      </div>
                      <Badge variant={inquiry.status === 'new' ? 'default' : 'outline'}>
                        {inquiry.status}
                      </Badge>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-2 text-sm">
                      {inquiry.organization && (
                        <p><strong>Organization:</strong> {inquiry.organization}</p>
                      )}
                      <p><strong>Curriculum:</strong> {inquiry.curriculum}</p>
                      <p><strong>Grade Range:</strong> {inquiry.grade_range}</p>
                      {inquiry.num_students && (
                        <p><strong>Number of Students:</strong> {inquiry.num_students}</p>
                      )}
                      <p><strong>Message:</strong> {inquiry.message}</p>
                      {inquiry.notes && (
                        <p className="text-muted-foreground"><strong>Notes:</strong> {inquiry.notes}</p>
                      )}
                    </div>
                    <div className="flex gap-2 mt-4">
                      <Button 
                        size="sm" 
                        variant="outline"
                        onClick={() => handleUpdateInquiryStatus(inquiry.id, 'contacted')}
                      >
                        Mark as Contacted
                      </Button>
                      <Button 
                        size="sm" 
                        variant="outline"
                        onClick={() => handleUpdateInquiryStatus(inquiry.id, 'converted')}
                      >
                        Mark as Converted
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              ))
            )}
          </div>
        ) : showLessonForm ? (
          <div>
            <h2 className="text-2xl font-semibold mb-4">
              {editingLesson ? 'Edit Lesson' : 'Create New Lesson'}
            </h2>
            <Card>
              <CardContent className="pt-6">
                <LessonForm
                  lesson={editingLesson}
                  onSave={handleSaveLesson}
                  onCancel={() => { setShowLessonForm(false); setEditingLesson(null); }}
                />
              </CardContent>
            </Card>
          </div>
        ) : (
          <div>
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-2xl font-semibold">Lessons ({lessons.length})</h2>
              <Button onClick={handleCreateNew}>+ Create New Lesson</Button>
            </div>
            <div className="space-y-4">
              {lessons.map(lesson => (
                <Card key={lesson.id}>
                  <CardHeader>
                    <div className="flex justify-between items-start">
                      <div>
                        <div className="flex gap-2 mb-2">
                          <Badge>{lesson.curriculum}</Badge>
                          <Badge variant="outline">Grade {lesson.grade}</Badge>
                          <Badge variant="outline">{lesson.subject}</Badge>
                        </div>
                        <CardTitle>{lesson.title.en}</CardTitle>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm text-muted-foreground mb-4">{lesson.description.en}</p>
                    <div className="flex gap-2">
                      <Button size="sm" variant="outline" onClick={() => navigate(`/lesson/${lesson.id}`)}>
                        View
                      </Button>
                      <Button size="sm" variant="outline" onClick={() => handleEditLesson(lesson)}>
                        Edit
                      </Button>
                      <Button size="sm" variant="destructive" onClick={() => handleDeleteLesson(lesson.id)}>
                        Delete
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              ))}</div>
          </div>
        )}
      </div>
    </div>
  );
}

export default AdminDashboard;
