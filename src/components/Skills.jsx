import { motion } from 'framer-motion';
import { skills } from '../data/portfolioData';
import './Skills.css';

const fadeUp = {
  hidden: { opacity: 0, y: 30 },
  visible: (i = 0) => ({
    opacity: 1,
    y: 0,
    transition: { duration: 0.5, delay: i * 0.1 },
  }),
};

export default function Skills() {
  const categories = Object.entries(skills);

  return (
    <section className="skills" id="skills">
      <div className="section-container">
        <motion.span
          className="section-label"
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: '-100px' }}
          variants={fadeUp}
        >
          Skills
        </motion.span>

        <motion.h2
          className="section-title"
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: '-100px' }}
          variants={fadeUp}
          custom={1}
        >
          Technologies I <span className="gradient-text">work with</span>
        </motion.h2>

        <div className="skills-grid">
          {categories.map(([category, items], idx) => (
            <motion.div
              key={category}
              className="skill-category-card glass-card"
              initial="hidden"
              whileInView="visible"
              viewport={{ once: true, margin: '-100px' }}
              variants={fadeUp}
              custom={idx + 1}
            >
              <div className="skill-category-title">{category}</div>
              <div className="skill-chips">
                {items.map((skill) => (
                  <span key={skill} className="skill-chip">
                    {skill}
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
