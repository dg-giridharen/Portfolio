import { motion } from 'framer-motion';
import { personalInfo, stats } from '../data/portfolioData';
import './About.css';

const fadeUp = {
  hidden: { opacity: 0, y: 30 },
  visible: (i = 0) => ({
    opacity: 1,
    y: 0,
    transition: { duration: 0.5, delay: i * 0.1 },
  }),
};

export default function About() {
  return (
    <section className="about" id="about">
      <div className="section-container">
        <motion.span
          className="section-label"
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: '-100px' }}
          variants={fadeUp}
        >
          About Me
        </motion.span>

        <motion.h2
          className="section-title"
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: '-100px' }}
          variants={fadeUp}
          custom={1}
        >
          Crafting software that <span className="gradient-text">scales</span>
        </motion.h2>

        <div className="about-grid">
          <motion.div
            className="about-text"
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: '-100px' }}
            variants={fadeUp}
            custom={2}
          >
            <div className="about-divider" />
            <p>
              {personalInfo.bio}
            </p>
            <p>
              Passionate about designing <strong>RESTful APIs, containerizing
              services with Docker/Kubernetes</strong>, and automating CI/CD
              workflows that power modern engineering teams.
            </p>
          </motion.div>

          <div className="about-stats">
            {stats.map((stat, i) => (
              <motion.div
                key={stat.label}
                className="about-stat-card glass-card"
                initial="hidden"
                whileInView="visible"
                viewport={{ once: true, margin: '-100px' }}
                variants={fadeUp}
                custom={i + 2}
              >
                <div className="about-stat-value">{stat.value}</div>
                <div className="about-stat-label">{stat.label}</div>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
