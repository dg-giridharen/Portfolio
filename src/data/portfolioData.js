export const personalInfo = {
  name: "Giridharen",
  fullName: "Giridharen Goguladhevan",
  tagline: "Software Engineer",
  taglineHighlight: "Cloud, DevOps & AI",
  location: "Chennai, India",
  email: "dg.giridharen@gmail.com",
  phone: "+91 73973 82046",
  github: "https://github.com/dg-giridharen",
  linkedin: "https://linkedin.com/in/dg-giridharen",
  bio: "Results-driven Software Engineer and dual-discipline Computer Science / Data Science student with hands-on experience architecting scalable backend systems, cloud-native infrastructure, and applied AI/ML pipelines. Proficient across Python, Java, C#, JavaScript/TypeScript, and the MERN stack, with demonstrated ability to design RESTful APIs, containerize services with Docker/Kubernetes, and automate CI/CD workflows.",
};

export const stats = [
  { value: "8.04", label: "CGPA at VIT" },
  { value: "2", label: "Internships" },
  { value: "7", label: "Languages" },
  { value: "3", label: "Projects Shipped" },
];

export const skills = {
  Languages: ["Python", "Java", "C#", "JavaScript", "TypeScript", "Go", "SQL"],
  "AI / ML": [
    "PyTorch",
    "TensorFlow",
    "Scikit-learn",
    "NumPy",
    "Pandas",
    "Transformers",
    "LLMs",
    "OpenCV",
  ],
  "Backend & Cloud": [
    "Node.js",
    "Express.js",
    ".NET",
    "FastAPI",
    "Flask",
    "Docker",
    "Kubernetes",
    "AWS",
    "PostgreSQL",
    "MongoDB",
    "Redis",
    "Terraform",
    "Jenkins",
  ],
  Frontend: ["React.js", "Next.js", "Vue.js", "HTML5/CSS3"],
  "Practices & Tools": ["Git/GitHub", "CI/CD", "RESTful API Design", "Microservices Architecture", "Agile/Scrum"],
};

export const experience = [
  {
    role: "Product Engineering Intern",
    company: "Kanini Software Solutions",
    period: "Jun 2026 – Present",
    description:
      "Collaborate with cross-functional product and engineering teams to translate business requirements into technical specifications, streamlining deployment workflows across releases. Drive scoped feature delivery through Agile sprint cycles, decomposing requirements into engineering milestones to accelerate release velocity. Engineer CRUD-based backend applications using C#, .NET Web API, and SQL, applying REST API design, database connectivity, and query optimization best practices, alongside front-end fundamentals (HTML5, CSS3, JavaScript ES6, Git/GitHub).",
  },
  {
    role: "MERN Stack Intern",
    company: "Destify",
    period: "Nov 2025 – Jan 2026",
    description:
      "Engineered full-stack modules and responsive web features using MongoDB, Express, React, and Node.js, ensuring clean API architecture and end-to-end data integrity. Implemented secure user authentication and dynamic content rendering for a production-facing application, collaborating with senior engineers to deliver scalable backend logic.",
  },
];

export const projects = [
  {
    title: "Lambda-Lite",
    subtitle: "Local FaaS (Function-as-a-Service) Platform",
    tech: ["React (Vite)", "FastAPI", "Docker", "PostgreSQL"],
    description:
      "Built a local-first Function-as-a-Service platform that uses FastAPI to orchestrate Docker containers, executing serverless functions without dependency on a cloud provider. Implemented predictive scheduling and cost-aware container TTL management backed by PostgreSQL, alongside a React (Vite) dashboard deployable independently on Vercel.",
  },
  {
    title: "DeployFlow",
    subtitle: "Self-Hosted Platform-as-a-Service (PaaS)",
    tech: ["Next.js", "TypeScript", "Express.js", "MongoDB", "Redis", "Docker", "Socket.IO"],
    description:
      "Built a self-hosted PaaS that automates containerized application deployment through GitHub/GitLab webhook integration and Docker-based build pipelines. Developed a real-time Next.js dashboard with WebSocket-driven deployment logs and live metrics, backed by a JWT/Google OAuth-secured Express.js API on MongoDB and Redis.",
  },
  {
    title: "Placement Portal",
    subtitle: "Full-Stack Application",
    tech: ["Vue.js", "Flask", "Python", "SQLite", "SQLAlchemy"],
    description:
      "Delivered a full-stack placement portal for students, recruiters, and administrators using Vue.js and Flask, featuring role-based access control for each user type. Engineered responsive Vue.js interfaces and RESTful Flask APIs for authentication, job postings, and application management, backed by a SQLite/SQLAlchemy relational database.",
  },
];

export const education = [
  {
    institution: "Vellore Institute of Technology (VIT), Chennai",
    degree: "B.Tech in Computer Science and Engineering",
    period: "2023 – 2027",
    score: "CGPA: 8.04",
  },
  {
    institution: "Indian Institute of Technology (IIT), Madras",
    degree: "Diploma in Programming",
    period: "2023 – 2026",
    score: null,
  },
  {
    institution: "Velammal Bodhi Campus, Kolapakkam",
    degree: "Higher Secondary (CBSE)",
    period: "2022 – 2023",
    score: "87.5%",
  },
  {
    institution: "Velammal Bodhi Campus, Kolapakkam",
    degree: "SSLC (CBSE)",
    period: "2020 – 2021",
    score: "90.6%",
  },
];
