import { motion } from 'framer-motion';
import { education } from '../data/portfolioData';
import './Education.css';

const fadeUp = {
  hidden: { opacity: 0, y: 30 },
  visible: (i = 0) => ({
    opacity: 1,
    y: 0,
    transition: { duration: 0.5, delay: i * 0.1 },
  }),
};

export default function Education() {
  return (
    <section className="education" id="education">
      <div className="section-container">
        <motion.span
          className="section-label"
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: '-100px' }}
          variants={fadeUp}
        >
          Education
        </motion.span>

        <motion.h2
          className="section-title"
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: '-100px' }}
          variants={fadeUp}
          custom={1}
        >
          Academic <span className="gradient-text">background</span>
        </motion.h2>

        <div className="education-grid">
          {education.map((item, idx) => (
            <motion.div
              key={item.institution + item.degree}
              className="education-card glass-card"
              initial="hidden"
              whileInView="visible"
              viewport={{ once: true, margin: '-100px' }}
              variants={fadeUp}
              custom={idx + 1}
            >
              <div className="education-period">{item.period}</div>
              <h3 className="education-institution">{item.institution}</h3>
              <p className="education-degree">{item.degree}</p>
              {item.score && (
                <span className="education-score">{item.score}</span>
              )}
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
