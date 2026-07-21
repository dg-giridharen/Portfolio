import { motion } from 'framer-motion';
import { FiGithub, FiLinkedin, FiMail, FiMapPin, FiPhone } from 'react-icons/fi';
import { personalInfo } from '../data/portfolioData';
import './Contact.css';

const fadeUp = {
  hidden: { opacity: 0, y: 30 },
  visible: (i = 0) => ({
    opacity: 1,
    y: 0,
    transition: { duration: 0.5, delay: i * 0.1 },
  }),
};

export default function Contact() {
  return (
    <section className="contact" id="contact">
      <div className="section-container">
        <motion.span
          className="section-label"
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: '-100px' }}
          variants={fadeUp}
        >
          Contact
        </motion.span>

        <motion.h2
          className="section-title"
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: '-100px' }}
          variants={fadeUp}
          custom={1}
        >
          Let&apos;s <span className="gradient-text">connect</span>
        </motion.h2>

        <motion.p
          className="section-subtitle"
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: '-100px' }}
          variants={fadeUp}
          custom={2}
        >
          I&apos;m always open to new opportunities, collaborations, and interesting
          conversations. Feel free to reach out!
        </motion.p>

        <motion.a
          href={`mailto:${personalInfo.email}`}
          className="contact-cta-btn"
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: '-100px' }}
          variants={fadeUp}
          custom={3}
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
        >
          <FiMail /> Say Hello
        </motion.a>

        <motion.div
          className="contact-details"
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: '-100px' }}
          variants={fadeUp}
          custom={4}
        >
          <a href={`mailto:${personalInfo.email}`} className="contact-detail">
            <FiMail className="contact-detail-icon" />
            <span>{personalInfo.email}</span>
          </a>
          <a href={`tel:${personalInfo.phone}`} className="contact-detail">
            <FiPhone className="contact-detail-icon" />
            <span>{personalInfo.phone}</span>
          </a>
          <span className="contact-detail">
            <FiMapPin className="contact-detail-icon" />
            <span>{personalInfo.location}</span>
          </span>
        </motion.div>

        <motion.div
          className="contact-socials"
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: '-100px' }}
          variants={fadeUp}
          custom={5}
        >
          <a
            href={personalInfo.github}
            target="_blank"
            rel="noopener noreferrer"
            className="contact-social-link"
            aria-label="GitHub"
          >
            <FiGithub />
          </a>
          <a
            href={personalInfo.linkedin}
            target="_blank"
            rel="noopener noreferrer"
            className="contact-social-link"
            aria-label="LinkedIn"
          >
            <FiLinkedin />
          </a>
          <a
            href={`mailto:${personalInfo.email}`}
            className="contact-social-link"
            aria-label="Email"
          >
            <FiMail />
          </a>
        </motion.div>

        <div className="contact-footer">
          <p>
            Designed & Built by{' '}
            <span className="gradient-text">{personalInfo.fullName}</span> ©{' '}
            {new Date().getFullYear()}
          </p>
        </div>
      </div>
    </section>
  );
}
