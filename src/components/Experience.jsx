import { motion } from 'framer-motion';
import { experience } from '../data/portfolioData';
import './Experience.css';

const fadeUp = {
  hidden: { opacity: 0, y: 30 },
  visible: (i = 0) => ({
    opacity: 1,
    y: 0,
    transition: { duration: 0.5, delay: i * 0.1 },
  }),
};

export default function Experience() {
  return (
    <section className="experience" id="experience">
      <div className="section-container">
        <motion.span
          className="section-label"
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: '-100px' }}
          variants={fadeUp}
        >
          Experience
        </motion.span>

        <motion.h2
          className="section-title"
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: '-100px' }}
          variants={fadeUp}
          custom={1}
        >
          Where I&apos;ve <span className="gradient-text">worked</span>
        </motion.h2>

        <div className="experience-timeline">
          {experience.map((item, idx) => (
            <motion.div
              key={item.company}
              className="experience-item"
              initial="hidden"
              whileInView="visible"
              viewport={{ once: true, margin: '-100px' }}
              variants={fadeUp}
              custom={idx + 1}
            >
              <div className="experience-header">
                <div>
                  <div className="experience-role">{item.role}</div>
                  <div className="experience-company">{item.company}</div>
                </div>
                <div className="experience-period">{item.period}</div>
              </div>
              <p className="experience-description">
                {item.description}
              </p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
