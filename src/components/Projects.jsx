import { motion } from 'framer-motion';
import { FiFolder } from 'react-icons/fi';
import { projects } from '../data/portfolioData';
import './Projects.css';

const fadeUp = {
  hidden: { opacity: 0, y: 30 },
  visible: (i = 0) => ({
    opacity: 1,
    y: 0,
    transition: { duration: 0.5, delay: i * 0.1 },
  }),
};

export default function Projects() {
  return (
    <section className="projects" id="projects">
      <div className="section-container">
        <motion.span
          className="section-label"
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: '-100px' }}
          variants={fadeUp}
        >
          Projects
        </motion.span>

        <motion.h2
          className="section-title"
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: '-100px' }}
          variants={fadeUp}
          custom={1}
        >
          Things I&apos;ve <span className="gradient-text">built</span>
        </motion.h2>

        <div className="projects-grid">
          {projects.map((project, idx) => (
            <motion.div
              key={project.title}
              className="project-card glass-card"
              initial="hidden"
              whileInView="visible"
              viewport={{ once: true, margin: '-100px' }}
              variants={fadeUp}
              custom={idx + 1}
            >
              <div className="project-icon">
                <FiFolder />
              </div>
              <h3 className="project-title">{project.title}</h3>
              <p className="project-subtitle">{project.subtitle}</p>
              <p className="project-description">
                {project.description}
              </p>
              <div className="project-tech-tags">
                {project.tech.map((t) => (
                  <span key={t} className="project-tech-tag">
                    {t}
                  </span>
                ))}
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
