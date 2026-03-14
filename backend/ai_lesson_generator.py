"""
AI Curriculum Lesson Generator
Generates comprehensive, age-appropriate AI lessons with multimedia content
Focus: Making AI simple and understandable for all children (ages 5-18)
"""

import json
from typing import List, Dict
import uuid

# Age group definitions
AGE_GROUPS = {
    "5-7": {"grades": ["K", "1", "2"], "complexity": "very_simple", "duration": 20},
    "8-9": {"grades": ["3", "4"], "complexity": "simple", "duration": 25},
    "10-12": {"grades": ["5", "6", "7"], "complexity": "moderate", "duration": 25},
    "13-15": {"grades": ["8", "9", "10"], "complexity": "intermediate", "duration": 30},
    "16-18": {"grades": ["11", "12"], "complexity": "advanced", "duration": 30}
}

# AI Curriculum Topics by Age Group
AI_CURRICULUM = {
    "5-7": [
        {
            "title": "What is Artificial Intelligence?",
            "description": "Learn what AI is through fun examples like Siri, Alexa, and smart toys",
            "keywords": ["AI basics", "friendly robots", "smart helpers"],
            "activities": ["Draw your dream robot", "Play with voice assistant", "Watch AI cartoon"],
            "concepts": ["Recognition", "Helping", "Learning"]
        },
        {
            "title": "AI Helpers in Our Home",
            "description": "Discover how AI helps us every day - from TV recommendations to smart speakers",
            "keywords": ["smart home", "voice assistants", "helpful AI"],
            "activities": ["Find AI devices at home", "Talk to Alexa/Siri", "Make a list of AI helpers"],
            "concepts": ["Voice recognition", "Smart devices", "Automation"]
        },
        {
            "title": "Pattern Recognition: How AI Sees",
            "description": "Learn how AI recognizes patterns - shapes, colors, and faces",
            "keywords": ["patterns", "shapes", "colors", "recognition"],
            "activities": ["Pattern matching game", "Find same shapes", "Face detection demo"],
            "concepts": ["Patterns", "Matching", "Visual recognition"]
        },
        {
            "title": "Teaching Computers: Like Teaching Pets",
            "description": "Understand how we teach AI, just like training a puppy to sit and stay",
            "keywords": ["training", "learning", "rewards"],
            "activities": ["Training game", "Reward and punishment", "Simple commands"],
            "concepts": ["Training", "Rewards", "Commands"]
        },
        {
            "title": "AI in Games: Smart Game Characters",
            "description": "Explore how AI makes video game characters smart and challenging",
            "keywords": ["gaming AI", "characters", "smart opponents"],
            "activities": ["Play simple AI game", "Observe AI behavior", "Design game character"],
            "concepts": ["Game AI", "Behavior", "Rules"]
        },
        {
            "title": "Sorting and Organizing with AI",
            "description": "Learn how AI helps sort things - toys, pictures, or songs",
            "keywords": ["sorting", "organizing", "categories"],
            "activities": ["Sort objects by color", "Group similar items", "Create collections"],
            "concepts": ["Sorting", "Categories", "Organization"]
        },
        {
            "title": "AI Artists: Computers That Draw",
            "description": "Discover how AI can create beautiful art and pictures",
            "keywords": ["AI art", "creativity", "drawing"],
            "activities": ["Use AI drawing tool", "Color by numbers", "Create AI artwork"],
            "concepts": ["Creativity", "Art", "Generation"]
        },
        {
            "title": "Friendly Robots: Our AI Friends",
            "description": "Meet different types of robots that help people - from vacuum cleaners to toys",
            "keywords": ["robots", "helpers", "machines"],
            "activities": ["Watch robot videos", "Design your robot", "Role play robot"],
            "concepts": ["Robotics", "Automation", "Helping"]
        },
        {
            "title": "AI Language: Talking to Computers",
            "description": "Learn how AI understands what we say and talks back to us",
            "keywords": ["speech", "language", "conversation"],
            "activities": ["Voice commands practice", "Chatbot conversation", "Language games"],
            "concepts": ["Speech", "Understanding", "Communication"]
        },
        {
            "title": "AI Safety: Being Smart with Smart Tech",
            "description": "Learn to use AI safely and kindly - basic digital citizenship",
            "keywords": ["safety", "privacy", "kindness"],
            "activities": ["Safety rules game", "Good vs bad AI use", "Permission practice"],
            "concepts": ["Safety", "Privacy", "Responsibility"]
        }
    ],
    "8-9": [
        {
            "title": "How Computers Learn: Machine Learning Basics",
            "description": "Understand the fundamentals of how computers learn from examples and data",
            "keywords": ["machine learning", "training", "examples", "data"],
            "activities": ["Teachable Machine demo", "Train simple classifier", "Pattern recognition game"],
            "concepts": ["Supervised learning", "Training data", "Pattern recognition"]
        },
        {
            "title": "AI Vision: How Computers See Images",
            "description": "Explore computer vision - how AI recognizes objects, faces, and scenes",
            "keywords": ["computer vision", "image recognition", "object detection"],
            "activities": ["Object detection demo", "Face recognition experiment", "Image classification"],
            "concepts": ["Computer vision", "Object detection", "Classification"]
        },
        {
            "title": "Chatbots and Virtual Assistants",
            "description": "Learn how AI chatbots understand questions and provide helpful answers",
            "keywords": ["chatbots", "NLP", "conversation", "assistants"],
            "activities": ["Build simple chatbot", "Test different assistants", "Design conversation flow"],
            "concepts": ["Natural language", "Intent recognition", "Responses"]
        },
        {
            "title": "AI in Gaming: Creating Smart Opponents",
            "description": "Discover how game developers use AI to make challenging and fun gameplay",
            "keywords": ["game AI", "pathfinding", "decision making"],
            "activities": ["Analyze game AI", "Simple pathfinding", "Design AI opponent"],
            "concepts": ["Game AI", "Decision trees", "Pathfinding"]
        },
        {
            "title": "Recommender Systems: How Netflix Knows What You Like",
            "description": "Understand how AI recommends movies, videos, and content you might enjoy",
            "keywords": ["recommendations", "preferences", "personalization"],
            "activities": ["Build recommendation system", "Analyze preferences", "Rate and predict"],
            "concepts": ["Collaborative filtering", "Preferences", "Predictions"]
        },
        {
            "title": "Introduction to Data Science",
            "description": "Learn what data is and how AI uses it to make smart decisions",
            "keywords": ["data", "information", "analysis", "patterns"],
            "activities": ["Collect data", "Create charts", "Find patterns"],
            "concepts": ["Data collection", "Analysis", "Visualization"]
        },
        {
            "title": "AI Music and Sound: Creating with Technology",
            "description": "Explore how AI creates music, recognizes songs, and understands sound",
            "keywords": ["AI music", "sound recognition", "audio"],
            "activities": ["AI music generator", "Sound classification", "Create melody"],
            "concepts": ["Audio processing", "Music generation", "Pattern recognition"]
        },
        {
            "title": "Smart Cities: AI in Our Communities",
            "description": "Discover how AI helps make cities safer, cleaner, and more efficient",
            "keywords": ["smart cities", "traffic", "infrastructure"],
            "activities": ["Design smart city", "Traffic simulation", "Problem solving"],
            "concepts": ["Urban AI", "Optimization", "Automation"]
        },
        {
            "title": "AI and Creativity: Art, Stories, and Design",
            "description": "Learn how AI assists artists, writers, and designers in creative work",
            "keywords": ["creativity", "art", "design", "generation"],
            "activities": ["AI art creation", "Story generation", "Design tool exploration"],
            "concepts": ["Generative AI", "Creativity", "Assistance"]
        },
        {
            "title": "Being Fair: AI Ethics for Kids",
            "description": "Understand fairness, bias, and making good choices with AI",
            "keywords": ["ethics", "fairness", "bias", "responsibility"],
            "activities": ["Fairness scenarios", "Bias detection game", "Decision making"],
            "concepts": ["Ethics", "Fairness", "Bias"]
        }
    ],
    "10-12": [
        {
            "title": "Neural Networks: How AI Thinks",
            "description": "Understand the brain-inspired structure that powers modern AI",
            "keywords": ["neural networks", "neurons", "layers", "learning"],
            "activities": ["Neuron simulation", "Build simple network", "Weight adjustment"],
            "concepts": ["Artificial neurons", "Layers", "Weights", "Activation"]
        },
        {
            "title": "Training AI Models: The Learning Process",
            "description": "Deep dive into how AI learns from data through training",
            "keywords": ["training", "datasets", "accuracy", "epochs"],
            "activities": ["Train classifier", "Test accuracy", "Adjust parameters"],
            "concepts": ["Training loop", "Loss function", "Optimization"]
        },
        {
            "title": "Computer Vision Applications",
            "description": "Explore real-world uses of computer vision in medicine, security, and daily life",
            "keywords": ["CV applications", "facial recognition", "medical imaging"],
            "activities": ["Object detection project", "Image segmentation", "Real-world examples"],
            "concepts": ["Detection", "Segmentation", "Classification"]
        },
        {
            "title": "Natural Language Processing: Understanding Text",
            "description": "Learn how AI reads, understands, and generates human language",
            "keywords": ["NLP", "text analysis", "sentiment", "translation"],
            "activities": ["Sentiment analysis", "Text classification", "Translation demo"],
            "concepts": ["Tokenization", "Embeddings", "Language models"]
        },
        {
            "title": "Reinforcement Learning: Learning by Doing",
            "description": "Discover how AI learns through trial and error, like humans do",
            "keywords": ["reinforcement learning", "rewards", "agents", "environments"],
            "activities": ["Game playing AI", "Reward design", "Policy learning"],
            "concepts": ["Agents", "Rewards", "Policies", "Q-learning"]
        },
        {
            "title": "Data Preprocessing and Preparation",
            "description": "Learn how to clean and prepare data for AI training",
            "keywords": ["data cleaning", "preprocessing", "features"],
            "activities": ["Clean dataset", "Feature engineering", "Data visualization"],
            "concepts": ["Data quality", "Feature extraction", "Normalization"]
        },
        {
            "title": "AI in Healthcare: Saving Lives with Technology",
            "description": "Explore how AI helps doctors diagnose diseases and find treatments",
            "keywords": ["medical AI", "diagnosis", "healthcare"],
            "activities": ["Medical image analysis", "Symptom checker", "Research exploration"],
            "concepts": ["Medical imaging", "Diagnosis", "Prediction"]
        },
        {
            "title": "Autonomous Systems: Self-Driving Cars",
            "description": "Understand how autonomous vehicles use AI to navigate safely",
            "keywords": ["autonomous vehicles", "sensors", "navigation"],
            "activities": ["Sensor simulation", "Path planning", "Safety scenarios"],
            "concepts": ["Perception", "Planning", "Control"]
        },
        {
            "title": "AI and Climate: Fighting Climate Change",
            "description": "Learn how AI helps monitor and combat environmental challenges",
            "keywords": ["climate AI", "environment", "sustainability"],
            "activities": ["Climate data analysis", "Prediction models", "Solution design"],
            "concepts": ["Environmental monitoring", "Prediction", "Optimization"]
        },
        {
            "title": "Bias and Fairness in AI Systems",
            "description": "Understand how bias enters AI and how to build fair systems",
            "keywords": ["bias", "fairness", "ethics", "discrimination"],
            "activities": ["Bias detection", "Fairness metrics", "Ethical scenarios"],
            "concepts": ["Algorithmic bias", "Fairness", "Mitigation"]
        }
    ],
    "13-15": [
        {
            "title": "Deep Learning Fundamentals",
            "description": "Master the foundations of deep neural networks and their applications",
            "keywords": ["deep learning", "CNNs", "RNNs", "architectures"],
            "activities": ["Build CNN", "Train deep network", "Architecture comparison"],
            "concepts": ["Convolutional networks", "Recurrent networks", "Backpropagation"]
        },
        {
            "title": "Building Your First AI Model",
            "description": "Complete project: Build, train, and deploy a real AI model",
            "keywords": ["model building", "training", "deployment"],
            "activities": ["Full project lifecycle", "Model training", "Testing and deployment"],
            "concepts": ["End-to-end ML", "Model deployment", "Evaluation"]
        },
        {
            "title": "Advanced Computer Vision: CNNs and Beyond",
            "description": "Deep dive into convolutional neural networks and modern CV techniques",
            "keywords": ["CNNs", "image segmentation", "object detection"],
            "activities": ["Implement CNN", "Transfer learning", "Object detection"],
            "concepts": ["Convolution", "Pooling", "Feature maps", "Transfer learning"]
        },
        {
            "title": "Transformer Models and Modern NLP",
            "description": "Understand the revolutionary transformer architecture behind ChatGPT",
            "keywords": ["transformers", "attention", "BERT", "GPT"],
            "activities": ["Attention mechanism", "Fine-tune model", "Text generation"],
            "concepts": ["Self-attention", "Transformers", "Pre-training"]
        },
        {
            "title": "Generative AI: Creating New Content",
            "description": "Explore GANs, diffusion models, and content generation",
            "keywords": ["GANs", "diffusion", "generation", "creativity"],
            "activities": ["Image generation", "Style transfer", "Creative AI"],
            "concepts": ["Generative models", "GANs", "Diffusion"]
        },
        {
            "title": "AI in Robotics: Physical Intelligence",
            "description": "Learn how AI powers robots to interact with the physical world",
            "keywords": ["robotics", "manipulation", "navigation"],
            "activities": ["Robot simulation", "Path planning", "Manipulation tasks"],
            "concepts": ["Robot perception", "Control", "Planning"]
        },
        {
            "title": "AI Ethics and Responsible Development",
            "description": "Critical examination of AI's impact on society and ethical considerations",
            "keywords": ["ethics", "responsibility", "impact", "governance"],
            "activities": ["Ethical case studies", "Debate sessions", "Policy design"],
            "concepts": ["AI ethics", "Governance", "Accountability"]
        },
        {
            "title": "AI in Science: Accelerating Discovery",
            "description": "How AI revolutionizes scientific research from physics to biology",
            "keywords": ["scientific AI", "research", "discovery"],
            "activities": ["Protein folding", "Drug discovery", "Pattern analysis"],
            "concepts": ["Scientific ML", "Discovery", "Simulation"]
        },
        {
            "title": "Explainable AI: Understanding Decisions",
            "description": "Learn techniques to interpret and explain AI model decisions",
            "keywords": ["XAI", "interpretability", "transparency"],
            "activities": ["SHAP analysis", "Feature importance", "Model interpretation"],
            "concepts": ["Explainability", "Interpretability", "Trust"]
        },
        {
            "title": "AI Careers: Future Opportunities",
            "description": "Explore career paths in AI and prepare for the future workforce",
            "keywords": ["careers", "jobs", "skills", "future"],
            "activities": ["Career research", "Skill mapping", "Project portfolio"],
            "concepts": ["Career paths", "Skills", "Industry"]
        }
    ],
    "16-18": [
        {
            "title": "Advanced Deep Learning Architectures",
            "description": "Master cutting-edge architectures: Vision Transformers, GPT, DALL-E",
            "keywords": ["ViT", "GPT", "DALL-E", "advanced architectures"],
            "activities": ["Implement ViT", "Fine-tune GPT", "Compare architectures"],
            "concepts": ["Vision Transformers", "Large language models", "Multimodal AI"]
        },
        {
            "title": "Production ML: Deploying AI Systems",
            "description": "Learn MLOps, deployment, monitoring, and maintaining AI in production",
            "keywords": ["MLOps", "deployment", "monitoring", "scaling"],
            "activities": ["Deploy model API", "Set up monitoring", "CI/CD pipeline"],
            "concepts": ["MLOps", "Deployment", "Monitoring", "Scaling"]
        },
        {
            "title": "Research Methods in AI",
            "description": "Learn how to read papers, conduct experiments, and contribute to AI research",
            "keywords": ["research", "papers", "experiments", "methodology"],
            "activities": ["Paper review", "Experiment design", "Result analysis"],
            "concepts": ["Scientific method", "Experimentation", "Publication"]
        },
        {
            "title": "Advanced NLP: Large Language Models",
            "description": "Deep dive into LLMs, prompt engineering, and fine-tuning",
            "keywords": ["LLMs", "GPT", "BERT", "prompt engineering"],
            "activities": ["Prompt engineering", "Fine-tuning LLM", "Evaluation"],
            "concepts": ["Language models", "Prompting", "Few-shot learning"]
        },
        {
            "title": "AI Safety and Alignment",
            "description": "Critical study of AI safety, alignment problems, and existential risks",
            "keywords": ["AI safety", "alignment", "risks", "control"],
            "activities": ["Safety scenarios", "Alignment problems", "Policy discussion"],
            "concepts": ["AI safety", "Value alignment", "Control problem"]
        },
        {
            "title": "Quantum Machine Learning",
            "description": "Introduction to quantum computing and its intersection with AI",
            "keywords": ["quantum", "QML", "quantum computing"],
            "activities": ["Quantum circuits", "QML algorithms", "Comparison study"],
            "concepts": ["Quantum computing", "Quantum algorithms", "Hybrid models"]
        },
        {
            "title": "AI for Social Good: Real-World Impact",
            "description": "Apply AI to solve global challenges: poverty, health, education",
            "keywords": ["social good", "impact", "development goals"],
            "activities": ["Impact project", "Problem analysis", "Solution design"],
            "concepts": ["AI for good", "Social impact", "Sustainable development"]
        },
        {
            "title": "Building AI Startups: Entrepreneurship",
            "description": "Learn to identify opportunities and build AI-powered businesses",
            "keywords": ["startups", "entrepreneurship", "business"],
            "activities": ["Pitch development", "MVP building", "Market analysis"],
            "concepts": ["Entrepreneurship", "Product-market fit", "Scaling"]
        },
        {
            "title": "AI Research Project: Capstone",
            "description": "Complete independent research project from ideation to publication",
            "keywords": ["research", "project", "independent work"],
            "activities": ["Research execution", "Paper writing", "Presentation"],
            "concepts": ["Research process", "Documentation", "Communication"]
        },
        {
            "title": "Future of AI: Trends and Predictions",
            "description": "Explore emerging trends, AGI, and preparing for an AI-driven future",
            "keywords": ["future", "AGI", "trends", "predictions"],
            "activities": ["Trend analysis", "Scenario planning", "Future mapping"],
            "concepts": ["AGI", "Future trends", "Technological singularity"]
        }
    ]
}


def generate_lesson_content(topic: Dict, age_group: str, grade: str) -> Dict:
    """Generate comprehensive lesson content"""
    
    complexity = AGE_GROUPS[age_group]["complexity"]
    duration = AGE_GROUPS[age_group]["duration"]
    
    # Generate detailed content based on complexity
    if complexity == "very_simple":
        content = f"""
## Welcome to: {topic['title']}! 🎉

### What You Will Learn Today:
{topic['description']}

### Story Time! 📖
Let me tell you about {topic['title'].lower()}...

Imagine you have a magical friend who can learn anything you teach them. That's what AI is like! 
Just like you learn to tie your shoes or count to 10, computers can learn too!

### Let's Explore! 🔍

**What is this about?**
{' '.join(topic['concepts'])} are like superpowers for computers. They help computers:
- See things (like recognizing your face in photos!)
- Hear things (like when you talk to Alexa!)
- Help you (like suggesting cartoons you might like!)

### Fun Activities! 🎨

Today we will:
{chr(10).join(f'{i+1}. {activity}' for i, activity in enumerate(topic['activities']))}

### Key Words to Remember: 📝
{', '.join(topic['keywords'])}

### Let's Practice! 💪

**Activity Time:**
- Try the interactive demo on the screen
- Play the matching game
- Draw your favorite AI helper

### What Did We Learn? ✅

We learned that:
- AI is like a smart helper
- Computers can learn just like us
- AI helps us in many fun ways!

### Home Fun! 🏠

Ask your parents to:
- Show you AI helpers at home
- Let you try talking to Siri or Alexa
- Find AI in your favorite games

Remember: AI is our friend and helper! Always be kind and safe when using technology. 💖

---

**Duration:** {duration} minutes
**Age Group:** {age_group} years old
"""
    
    elif complexity == "simple":
        content = f"""
## Lesson: {topic['title']}

### Learning Objectives 🎯
By the end of this lesson, you will understand:
- {topic['description']}
- How {topic['concepts'][0].lower()} works in real life
- Ways to use AI in your daily activities

### Introduction 📚

{topic['title']} is an exciting part of Artificial Intelligence that helps computers do amazing things!

Think about your favorite game. Did you know that AI might be making it more fun? Or when you search for videos online, AI helps find exactly what you want to watch!

### Main Content 🧠

**Understanding the Basics:**

{topic['concepts'][0]} is when computers:
1. Collect information (called "data")
2. Learn patterns from that information
3. Make decisions or predictions
4. Get better over time with practice

**Real-World Examples:**

Let's see where we find this:
- **At Home:** Smart speakers, photo apps, game recommendations
- **At School:** Educational apps, spelling checkers, math helpers
- **In Games:** Smart opponents, helpful hints, level adjustments

### Hands-On Activities 🎮

**Activity 1: {topic['activities'][0]}**
- Step 1: Observe how AI works
- Step 2: Try it yourself
- Step 3: Notice the patterns

**Activity 2: {topic['activities'][1]}**
- Experiment with different inputs
- See how AI responds
- Compare results

**Activity 3: {topic['activities'][2]}**
- Create your own example
- Test and improve
- Share with classmates

### Important Concepts 🔑

**Keywords to Know:**
{chr(10).join(f'- **{keyword.title()}**: A key part of {topic["title"].lower()}' for keyword in topic['keywords'])}

### STEAM Connection 🎨

How does this relate to STEAM?
- **Science:** Understanding how AI learns
- **Technology:** Using computers and devices
- **Engineering:** Building AI systems
- **Arts:** Creating with AI tools
- **Mathematics:** Patterns and data

### Challenge Time! 🏆

Try this:
1. Find 3 examples of AI in your life
2. Explain how they help you
3. Think about how they might improve

### Review and Reflect 📝

**What We Learned:**
- {topic['concepts'][0]} helps computers learn
- AI is in many places around us
- We can use AI to solve problems

**Think About:**
- How can AI make your life easier?
- What would you teach an AI to do?
- How can we use AI responsibly?

### Home Practice 🏠

This week:
- Try the suggested activities at home
- Observe AI in action
- Share what you learned with family

---

**Duration:** {duration} minutes
**Age Range:** {age_group} years
**Difficulty:** {complexity.replace('_', ' ').title()}
"""
    
    elif complexity == "moderate":
        content = f"""
## {topic['title']}

### Lesson Overview 📋

**Duration:** {duration} minutes  
**Age Group:** {age_group} years  
**Prerequisites:** Basic understanding of computers and data

### Learning Objectives 🎯

Upon completion, students will be able to:
1. Explain {topic['description'].lower()}
2. Identify key components of {topic['concepts'][0].lower()}
3. Apply concepts through practical demonstrations
4. Analyze real-world applications
5. Create simple projects using these principles

### Introduction (5 minutes) 🌟

**What is {topic['title']}?**

{topic['description']}

In today's digital world, {topic['title'].lower()} represents one of the most powerful and widely-used applications of Artificial Intelligence. From the apps on your phone to the games you play, these concepts are everywhere!

**Why This Matters:**

Understanding {topic['concepts'][0].lower()} helps you:
- Recognize AI in daily life
- Make informed decisions about technology
- Prepare for future careers in tech
- Create your own AI-powered projects

### Core Concepts (10 minutes) 🧠

**1. {topic['concepts'][0]}**

This is the foundation of {topic['title'].lower()}. It involves:
- **Data Collection:** Gathering information from various sources
- **Pattern Recognition:** Finding similarities and differences
- **Learning Algorithm:** The mathematical process that enables improvement
- **Prediction/Decision:** Using learned patterns to make choices

**2. {topic['concepts'][1] if len(topic['concepts']) > 1 else 'Application'}**

How these concepts work together:
- Input data flows through the system
- Algorithms process the information
- Patterns emerge from the data
- Outputs are generated and refined

**3. {topic['concepts'][2] if len(topic['concepts']) > 2 else 'Real-World Use'}**

Practical applications include:
- Healthcare: Disease diagnosis and treatment
- Transportation: Navigation and autonomous vehicles
- Entertainment: Personalized recommendations
- Education: Adaptive learning systems
- Environment: Climate prediction and conservation

### Technical Deep Dive (8 minutes) 🔬

**How It Works:**

```
Step 1: DATA PREPARATION
- Collect relevant data
- Clean and organize information
- Split into training and testing sets

Step 2: TRAINING PROCESS
- Feed data to the AI model
- Adjust internal parameters
- Minimize errors and improve accuracy

Step 3: EVALUATION
- Test with new data
- Measure performance
- Refine and optimize

Step 4: DEPLOYMENT
- Use in real-world scenarios
- Monitor performance
- Continuous improvement
```

**Key Technologies:**

- {topic['keywords'][0].title()}: Core technology enabling the system
- {topic['keywords'][1].title() if len(topic['keywords']) > 1 else 'AI Framework'}: Supporting framework for functionality  
- {topic['keywords'][2].title() if len(topic['keywords']) > 2 else 'Tools'}: Tools for implementation

### Hands-On Activities (15 minutes) 🎨

**Activity 1: {topic['activities'][0]}**

Objective: Understand the basic principles through interaction

Instructions:
1. Access the online tool/demo
2. Input various examples
3. Observe how the system responds
4. Note patterns and behaviors
5. Experiment with edge cases

**Activity 2: {topic['activities'][1]}**

Objective: Apply concepts to a practical problem

Instructions:
1. Define a simple problem to solve
2. Gather or create sample data
3. Use available tools to train a model
4. Test accuracy and refine
5. Document your results

**Activity 3: {topic['activities'][2]}**

Objective: Creative application and innovation

Instructions:
1. Brainstorm a unique application
2. Design the system architecture
3. Plan implementation steps
4. Create a prototype or detailed plan
5. Present to class

### STEAM Integration 🌈

**Science Connection:**
- Hypothesis testing with AI models
- Experimental design and validation
- Understanding causation vs correlation

**Technology Connection:**
- Programming and algorithms
- Data structures and processing
- System architecture

**Engineering Connection:**
- Problem-solving methodology
- Design thinking approach
- Optimization and efficiency

**Arts Connection:**
- Creative AI applications
- Generative art and music
- Human-AI collaboration

**Mathematics Connection:**
- Statistics and probability
- Linear algebra fundamentals
- Optimization techniques

### Real-World Case Studies 📊

**Case Study 1: {topic['keywords'][0].title()} in Action**
- Industry application
- Problem solved
- Impact and results
- Lessons learned

**Case Study 2: Innovative Use of {topic['concepts'][0]}**
- Unique implementation
- Challenges overcome
- Future potential
- Your ideas for improvement

### Ethical Considerations ⚖️

When working with AI, we must consider:
- **Privacy:** How is data collected and used?
- **Fairness:** Does the system treat everyone equally?
- **Transparency:** Can we understand how decisions are made?
- **Safety:** What are the potential risks?
- **Responsibility:** Who is accountable for AI actions?

### Assessment and Review (7 minutes) ✅

**Knowledge Check:**
1. What are the key components of {topic['concepts'][0].lower()}?
2. How does {topic['title'].lower()} apply to real-world problems?
3. What ethical considerations are important?

**Reflection Questions:**
- What surprised you most about this lesson?
- How might you use these concepts in a project?
- What questions do you still have?

**Project Ideas:**
- Build a simple classifier for [relevant topic]
- Create a presentation on AI ethics
- Design an AI system to solve a school problem

### Resources for Further Learning 📚

**Free Tools:**
- Teachable Machine (Google)
- Scratch AI extensions
- Code.org AI curriculum

**Videos:**
- Khan Academy: AI fundamentals
- CrashCourse: Computer Science
- 3Blue1Brown: Neural networks

**Websites:**
- AI4K12.org
- MIT RAISE resources
- Elements of AI (free course)

### Home Assignment 🏠

**This Week:**
1. Complete the online interactive tutorial
2. Find 5 examples of AI in your life
3. Write a short reflection (200 words)
4. Prepare questions for next lesson

**Optional Challenge:**
- Build a simple AI project
- Research a specific application
- Interview someone who works with AI

---

**Key Takeaways:**
- {topic['concepts'][0]} is fundamental to modern AI
- Real-world applications are everywhere
- Ethics and responsibility matter
- Anyone can learn and create with AI

**Next Lesson Preview:**
We'll build on today's concepts to explore [related topic]!

---

**Duration:** {duration} minutes  
**Complexity:** {complexity.replace('_', ' ').title()}
"""
    
    else:  # intermediate or advanced
        content = f"""
# {topic['title']}

## Course Information
- **Duration:** {duration} minutes
- **Level:** {complexity.replace('_', ' ').title()}
- **Age Group:** {age_group} years
- **Prerequisites:** Understanding of basic ML concepts, programming experience recommended

---

## Abstract

{topic['description']} This comprehensive lesson explores the theoretical foundations, practical implementations, and cutting-edge applications of {topic['concepts'][0].lower()} in modern artificial intelligence systems.

## Learning Outcomes 🎯

By the end of this lesson, students will:

1. **Understand** the theoretical underpinnings of {topic['concepts'][0].lower()}
2. **Analyze** complex AI architectures and their components
3. **Implement** functional AI models using industry-standard tools
4. **Evaluate** performance metrics and optimization strategies
5. **Synthesize** knowledge to design novel solutions
6. **Critically assess** ethical implications and societal impact

## Module 1: Theoretical Foundations (8 minutes) 🧮

### 1.1 Historical Context

The development of {topic['title'].lower()} represents a significant milestone in AI evolution:

- **Early Foundations (1950s-1980s):** Pioneering work in [relevant field]
- **Modern Breakthroughs (1990s-2010s):** Key algorithmic innovations
- **Current State (2020s):** State-of-the-art approaches and capabilities
- **Future Directions:** Emerging trends and research frontiers

### 1.2 Mathematical Framework

**Core Principles:**

The mathematical foundation of {topic['concepts'][0].lower()} rests on:

```
Key Equation: [Simplified representation]
f(x) = Model(input, parameters, context)

Where:
- x = input data
- f(x) = output/prediction
- Model = learned function
- parameters = weights and biases
- context = additional information
```

**Important Concepts:**

1. **{topic['keywords'][0].title()}**
   - Definition and significance
   - Mathematical representation
   - Computational complexity

2. **{topic['keywords'][1].title() if len(topic['keywords']) > 1 else 'AI Technology'}**
   - Role in the system
   - Implementation strategies
   - Trade-offs and considerations

3. **{topic['keywords'][2].title() if len(topic['keywords']) > 2 else 'Advanced Tools'}**
   - Advanced applications
   - State-of-the-art techniques
   - Open research problems

### 1.3 Algorithmic Approaches

**Primary Algorithms:**

1. **Algorithm A: [Specific technique]**
   - Time complexity: O(n log n)
   - Space complexity: O(n)
   - Best use cases: [examples]

2. **Algorithm B: [Alternative approach]**
   - Advantages over Algorithm A
   - Limitations and constraints
   - Hybrid approaches

## Module 2: Technical Implementation (12 minutes) 💻

### 2.1 System Architecture

**High-Level Design:**

```
[Input Layer] → [Processing Pipeline] → [Output Layer]
     ↓                    ↓                    ↓
Data Prep          Feature Extraction    Post-Processing
Validation         Model Inference       Result Formatting
```

**Components:**

1. **Data Pipeline**
   - Ingestion and validation
   - Preprocessing and augmentation
   - Feature engineering
   - Data versioning

2. **Model Architecture**
   - Layer design and connectivity
   - Activation functions
   - Regularization techniques
   - Optimization strategies

3. **Inference System**
   - Batch vs real-time processing
   - Scalability considerations
   - Latency optimization
   - Resource management

### 2.2 Code Implementation

**Practical Example:**

```python
# Pseudocode for {topic['title']}
import ai_framework as ai

# 1. Data Preparation
data = ai.load_dataset('{topic["keywords"][0]}')
train, test = ai.split(data, ratio=0.8)

# 2. Model Definition
model = ai.{topic['concepts'][0].replace(' ', '')}(
    input_size=data.features,
    hidden_layers=[128, 64, 32],
    output_size=data.classes
)

# 3. Training Process
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

history = model.train(
    train_data=train,
    epochs=50,
    validation_split=0.2,
    callbacks=[early_stopping, model_checkpoint]
)

# 4. Evaluation
test_results = model.evaluate(test_data=test)
print("Test Accuracy: ", test_results['accuracy'])

# 5. Deployment
model.save('production_model.pkl')
api.deploy(model, endpoint='/predict')
```

### 2.3 Optimization Techniques

**Performance Enhancement:**

- **Hyperparameter Tuning:** Grid search, random search, Bayesian optimization
- **Architecture Search:** Neural Architecture Search (NAS), AutoML
- **Training Strategies:** Transfer learning, curriculum learning, meta-learning
- **Computational Efficiency:** Pruning, quantization, knowledge distillation

## Module 3: Advanced Applications (15 minutes) 🚀

### 3.1 Industry Use Cases

**Healthcare Application:**
- Problem: [Specific medical challenge]
- AI Solution: {topic['concepts'][0]} for diagnosis/treatment
- Impact: Improved accuracy, reduced costs, saved lives
- Challenges: Data privacy, regulatory approval, clinical validation

**Business Application:**
- Problem: [Specific business need]
- AI Solution: Intelligent automation and decision support
- Impact: Increased efficiency, better insights, competitive advantage
- Challenges: Integration, change management, ROI measurement

**Research Application:**
- Problem: [Scientific question]
- AI Solution: Accelerating discovery and analysis
- Impact: New findings, validated hypotheses, published research
- Challenges: Reproducibility, interpretability, domain expertise

### 3.2 Cutting-Edge Research

**Recent Breakthroughs:**

1. **Advancement in {topic['keywords'][0]}** (2024)
   - Research team and institution
   - Key innovation
   - Performance improvements
   - Future implications

2. **Novel Application of {topic['concepts'][1] if len(topic['concepts']) > 1 else 'AI'}**
   - Unconventional approach
   - Results and validation
   - Potential for broader impact

### 3.3 Hands-On Projects

**Project 1: {topic['activities'][0]}**

**Objective:** Build a production-ready AI system

**Requirements:**
- Dataset of at least 10,000 samples
- 85%+ accuracy on test set
- < 100ms inference latency
- Documentation and code repository

**Steps:**
1. Problem definition and scope
2. Data collection and preparation
3. Model architecture design
4. Training and validation
5. Optimization and deployment
6. Monitoring and maintenance

**Deliverables:**
- Functional code (GitHub repository)
- Technical documentation
- Performance analysis report
- Demo video or presentation

**Project 2: {topic['activities'][1]}**

**Objective:** Research exploration and innovation

**Focus Areas:**
- Novel algorithmic approaches
- Unique data modalities
- Cross-domain applications
- Ethical AI implementation

**Project 3: {topic['activities'][2]}**

**Objective:** Collaborative team project

**Team Roles:**
- Data Engineer
- ML Engineer
- Research Scientist
- Product Manager
- Ethics Reviewer

## Module 4: Ethics, Impact & Future (10 minutes) ⚖️

### 4.1 Ethical Framework

**Core Principles:**

1. **Transparency & Explainability**
   - Model interpretability techniques
   - Stakeholder communication
   - Decision auditability

2. **Fairness & Bias Mitigation**
   - Demographic parity
   - Equal opportunity
   - Predictive equality
   - Bias detection and correction

3. **Privacy & Security**
   - Data protection regulations (GDPR, CCPA)
   - Differential privacy
   - Federated learning
   - Secure multi-party computation

4. **Accountability & Governance**
   - Responsible AI frameworks
   - Impact assessments
   - Stakeholder involvement
   - Regulatory compliance

### 4.2 Societal Impact

**Positive Impacts:**
- Improved healthcare outcomes
- Enhanced accessibility
- Scientific advancement
- Economic opportunities

**Potential Risks:**
- Job displacement
- Surveillance concerns
- Algorithmic discrimination
- Environmental costs (energy consumption)

**Mitigation Strategies:**
- Education and reskilling programs
- Regulatory frameworks
- Multi-stakeholder governance
- Sustainable AI practices

### 4.3 Future Outlook

**Emerging Trends:**

1. **Trend 1: [Specific development]**
   - Current status
   - Expected timeline
   - Potential impact

2. **Trend 2: [Another advancement]**
   - Research directions
   - Technical challenges
   - Societal considerations

**Your Role in the Future:**
- Career opportunities in AI
- Interdisciplinary collaboration
- Continuous learning and adaptation
- Ethical leadership

## Assessment & Evaluation ✅

### Knowledge Assessment

**Conceptual Questions:**
1. Explain the key differences between [concept A] and [concept B]
2. Analyze the trade-offs in [specific scenario]
3. Design a system architecture for [given problem]

**Technical Questions:**
1. Implement [specific algorithm] from scratch
2. Debug and optimize [provided code]
3. Compare performance of [different approaches]

**Critical Thinking:**
1. Evaluate ethical implications of [use case]
2. Propose solutions to [open research problem]
3. Assess societal impact of [technology trend]

### Practical Assessment

**Project Evaluation Criteria:**
- Technical correctness (30%)
- Innovation and creativity (20%)
- Code quality and documentation (20%)
- Performance and efficiency (15%)
- Presentation and communication (15%)

## Resources & Further Learning 📚

### Essential Reading

**Academic Papers:**
1. [Seminal paper on topic] - Author et al. (Year)
2. [Recent breakthrough] - Research team (2024)
3. [Comprehensive survey] - Review article

**Books:**
1. "Deep Learning" - Goodfellow, Bengio, Courville
2. "Hands-On Machine Learning" - Aurélien Géron
3. "[Relevant specialized book]" - Author

### Online Resources

**Courses:**
- Coursera: Deep Learning Specialization (Andrew Ng)
- Fast.ai: Practical Deep Learning
- MIT OpenCourseWare: AI and ML courses

**Tools & Frameworks:**
- TensorFlow / PyTorch
- Scikit-learn
- Hugging Face Transformers
- Weights & Biases (experiment tracking)

**Communities:**
- Papers with Code
- ArXiv.org (research papers)
- Reddit: r/MachineLearning
- GitHub: trending ML repositories

### Datasets

**Public Datasets:**
- ImageNet, CIFAR, MNIST (vision)
- GLUE, SQuAD (NLP)
- [Domain-specific datasets]

**Data Sources:**
- Kaggle competitions
- Google Dataset Search
- Academic repositories
- Government open data

## Home Assignment 🏠

### Required Work

**1. Research Paper Review**
- Select a recent paper on {topic['title'].lower()}
- Write a 500-word critical analysis
- Present key findings and limitations

**2. Implementation Project**
- Build a functional system using concepts from this lesson
- Document design decisions
- Achieve specified performance targets

**3. Ethical Analysis**
- Choose a controversial AI application
- Analyze from multiple ethical perspectives
- Propose governance recommendations

### Optional Challenges

**Advanced Implementations:**
- Replicate a state-of-the-art model
- Contribute to an open-source project
- Participate in a Kaggle competition

**Research Exploration:**
- Investigate an open problem
- Propose novel approaches
- Design experiments to validate hypotheses

---

## Summary & Key Takeaways

**Core Concepts Mastered:**
- {topic['concepts'][0]} and its applications
- Technical implementation strategies
- Ethical considerations and societal impact
- Future trends and opportunities

**Skills Developed:**
- Theoretical understanding
- Practical implementation
- Critical analysis
- Ethical reasoning
- Innovation and creativity

**Next Steps:**
- Continue hands-on practice
- Engage with research community
- Build a portfolio of projects
- Stay updated with latest developments

---

## Lesson Metadata

**Difficulty:** {complexity.replace('_', ' ').title()}  
**Duration:** {duration} minutes  
**Format:** Lecture + Hands-on + Discussion  
**Assessment:** Projects + Presentations + Written work

**Keywords:** {', '.join(topic['keywords'])}

**Prerequisites:**
- Programming proficiency (Python recommended)
- Linear algebra and calculus basics
- Statistics and probability fundamentals
- Prior ML/AI coursework helpful

**Related Topics:**
- [Connected concept 1]
- [Connected concept 2]
- [Advanced follow-up topic]

---

*This lesson is part of the Global AI Education Initiative*  
*Preparing the next generation for an AI-driven future*  
*© 2024 TEC Sri Lanka Worldwide - Open Educational Resource*
"""
    
    return {
        "id": str(uuid.uuid4()),
        "curriculum": "AI-STEAM",
        "subject": "artificial_intelligence",
        "grade": grade,
        "age_group": age_group,
        "difficulty": complexity,
        "estimated_duration": duration,
        "title": {
            "en": topic['title']
        },
        "description": {
            "en": topic['description']
        },
        "content": {
            "en": content
        },
        "keywords": topic['keywords'],
        "concepts": topic['concepts'],
        "activities": topic['activities'],
        "media": {
            "videos": [],  # Will be populated with relevant YouTube links
            "images": [],  # Will be populated with diagrams
            "diagrams": []  # Will be generated or sourced
        },
        "source": "AI-STEAM Global Curriculum",
        "source_url": "https://github.com/tecsrilankaworldwide/steam-curriculum-hub",
        "license": "CC BY 4.0",
        "created_at": "2024-03-11T17:00:00Z",
        "language_support": ["en", "si", "ta", "hi", "es", "fr", "de", "ar", "zh", "ja", "ko"]
    }


def generate_all_lessons() -> List[Dict]:
    """Generate all 50 lessons across age groups"""
    all_lessons = []
    
    for age_group, topics in AI_CURRICULUM.items():
        grade = AGE_GROUPS[age_group]["grades"][0]  # Use first grade in range
        
        for topic in topics:
            lesson = generate_lesson_content(topic, age_group, grade)
            all_lessons.append(lesson)
    
    return all_lessons


if __name__ == "__main__":
    import os as _os
    _script_dir = _os.path.dirname(_os.path.abspath(__file__))
    print("🎓 Generating 50 AI-STEAM Curriculum Lessons...")
    lessons = generate_all_lessons()
    
    # Save to JSON
    _output_path = _os.path.join(_script_dir, 'ai_lessons_batch1.json')
    with open(_output_path, 'w', encoding='utf-8') as f:
        json.dump(lessons, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Generated {len(lessons)} lessons successfully!")
    print(f"📊 Breakdown by age group:")
    for age_group in AGE_GROUPS.keys():
        count = len([l for l in lessons if l['age_group'] == age_group])
        print(f"   - Ages {age_group}: {count} lessons")
