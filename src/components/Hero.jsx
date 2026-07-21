import { motion } from 'framer-motion';
import { FiGithub, FiLinkedin, FiMail } from 'react-icons/fi';
import { personalInfo } from '../data/portfolioData';
import './Hero.css';

export default function Hero() {
  return (
    <section className="hero" id="hero">
      <div className="hero-container">
        <div className="hero-grid">
          <motion.div
            className="hero-avatar-wrapper"
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.7, delay: 0.2 }}
          >
            <div className="hero-avatar">
              <img src="/profile.png" alt="Giridharen Goguladhevan" />
            </div>
          </motion.div>

          <div className="hero-text-block">
            <motion.p
              className="hero-greeting"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.3 }}
            >
              Hello, I&apos;m
            </motion.p>

            <motion.h1
              className="hero-name"
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.7, delay: 0.5 }}
            >
              <span className="gradient-text">{personalInfo.name}</span>
            </motion.h1>

            <motion.p
              className="hero-tagline"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.7 }}
            >
              {personalInfo.tagline} · <span>{personalInfo.taglineHighlight}</span>
            </motion.p>

            <motion.div
              className="hero-socials"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.9 }}
            >
              <a
                href={personalInfo.github}
                target="_blank"
                rel="noopener noreferrer"
                className="hero-social-link"
                aria-label="GitHub"
              >
                <FiGithub />
              </a>
              <a
                href={personalInfo.linkedin}
                target="_blank"
                rel="noopener noreferrer"
                className="hero-social-link"
                aria-label="LinkedIn"
              >
                <FiLinkedin />
              </a>
              <a
                href={`mailto:${personalInfo.email}`}
                className="hero-social-link"
                aria-label="Email"
              >
                <FiMail />
              </a>
            </motion.div>
          </div>
        </div>

        <motion.a
          href="#about"
          className="hero-scroll-indicator"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.6, delay: 1.2 }}
        >
          <span>Scroll</span>
          <div className="hero-scroll-line" />
        </motion.a>
      </div>
    </section>
  );
}
