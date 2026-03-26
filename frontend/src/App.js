import "@/App.css";
import { useState } from "react";
import { motion } from "framer-motion";
import { Toaster, toast } from "sonner";
import axios from "axios";
import { ArrowRight, Check, Clock, Brain, Zap, Bot, Sparkles, Gift } from "lucide-react";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const PANDA_LOGO = "https://customer-assets.emergentagent.com/job_22990b85-c24e-49bf-a598-fc26b361df44/artifacts/jkf5exp1_WhatsApp%20Image%202026-03-24%20at%209.09.53%20PM.jpeg";

const fadeInUp = {
  hidden: { opacity: 0, y: 30 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.6, ease: "easeOut" } }
};

const staggerContainer = {
  hidden: { opacity: 0 },
  visible: { opacity: 1, transition: { staggerChildren: 0.15 } }
};

const pandaFloat = {
  animate: {
    y: [-8, 8, -8],
    scale: [1, 1.02, 1],
    transition: { duration: 4, repeat: Infinity, ease: "easeInOut" }
  }
};

// Hero Section
const HeroSection = () => {
  const scrollToWaitlist = () => {
    document.getElementById('waitlist')?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <section data-testid="hero-section" className="min-h-screen flex flex-col lg:flex-row items-center justify-between px-6 md:px-12 lg:px-24 py-20 lg:py-0">
      <motion.div
        className="lg:w-1/2 text-left"
        initial="hidden"
        animate="visible"
        variants={staggerContainer}
      >
        <motion.div
          variants={fadeInUp}
          className="inline-block px-4 py-2 bg-[#0A0A0A] text-[#FAFAFA] rounded-full text-xs tracking-widest uppercase mb-8"
          style={{ fontFamily: "'JetBrains Mono', monospace" }}
        >
          <Sparkles className="w-3 h-3 inline mr-2" />
          something big is cooking
        </motion.div>

        <motion.h1
          variants={fadeInUp}
          className="text-5xl md:text-6xl lg:text-7xl xl:text-8xl font-black leading-[0.9] mb-8"
          style={{ fontFamily: "'Outfit', sans-serif" }}
        >
          apply smarter.
          <br />
          <span className="text-[#888]">not harder.</span>
        </motion.h1>

        <motion.p
          variants={fadeInUp}
          className="text-base md:text-lg text-[#666] max-w-md mb-8"
          style={{ fontFamily: "'JetBrains Mono', monospace" }}
        >
          ai scans your resume. finds perfect matches. applies on your behalf. zero effort from you.
        </motion.p>

        <motion.div
          variants={fadeInUp}
          className="flex flex-wrap gap-6 mb-10 text-xs text-[#888]"
          style={{ fontFamily: "'JetBrains Mono', monospace" }}
        >
          <span className="flex items-center gap-2"><Clock className="w-3 h-3" /> 200+ hrs saved</span>
          <span className="flex items-center gap-2"><Zap className="w-3 h-3" /> 50 apply/day</span>
          <span className="flex items-center gap-2"><Bot className="w-3 h-3" /> fully automatic</span>
        </motion.div>

        <motion.button
          variants={fadeInUp}
          data-testid="hero-cta-btn"
          onClick={scrollToWaitlist}
          className="btn-invert px-8 py-4 rounded-full text-base font-semibold flex items-center gap-2"
          style={{ fontFamily: "'Outfit', sans-serif" }}
        >
          join waitlist <ArrowRight className="w-4 h-4" />
        </motion.button>
      </motion.div>

      <motion.div
        className="lg:w-1/2 flex justify-center lg:justify-end mt-16 lg:mt-0"
        variants={pandaFloat}
        animate="animate"
      >
        <img
          data-testid="hero-panda-logo"
          src={PANDA_LOGO}
          alt="LazyBot Panda"
          className="w-64 md:w-80 lg:w-[420px] object-contain"
        />
      </motion.div>
    </section>
  );
};

// The Struggle Section
const StruggleSection = () => {
  return (
    <section data-testid="struggle-section" className="py-24 md:py-32 px-6 md:px-12 lg:px-24 bg-[#0A0A0A] text-[#FAFAFA]">
      <motion.div
        className="max-w-4xl"
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: "-100px" }}
        variants={staggerContainer}
      >
        <motion.h2
          variants={fadeInUp}
          className="text-3xl md:text-5xl lg:text-6xl font-black mb-12 leading-tight"
          style={{ fontFamily: "'Outfit', sans-serif" }}
        >
          job hunting rn is giving
          <br />
          <span className="text-[#666]">unpaid internship energy.</span>
        </motion.h2>

        <motion.div
          variants={fadeInUp}
          className="grid grid-cols-2 md:grid-cols-4 gap-4"
        >
          {[
            { num: "6-12", label: "hrs wasted per 50 applications" },
            { num: "200+", label: "hrs lost monthly" },
            { num: "80%", label: "applications ghosted" },
            { num: "∞", label: "times same info typed" }
          ].map((stat, i) => (
            <div key={i} className="text-center p-4" data-testid={`stat-${i + 1}`}>
              <p className="text-3xl md:text-4xl font-black" style={{ fontFamily: "'Outfit', sans-serif" }}>{stat.num}</p>
              <p className="text-xs text-[#888] mt-1" style={{ fontFamily: "'JetBrains Mono', monospace" }}>{stat.label}</p>
            </div>
          ))}
        </motion.div>
      </motion.div>
    </section>
  );
};

// How It Hits Different Section
const SolutionSection = () => {
  return (
    <section data-testid="solution-section" className="py-24 md:py-32 px-6 md:px-12 lg:px-24">
      <motion.div
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: "-100px" }}
        variants={staggerContainer}
        className="max-w-5xl"
      >
        <motion.h2
          variants={fadeInUp}
          className="text-3xl md:text-5xl lg:text-6xl font-black mb-16 leading-tight"
          style={{ fontFamily: "'Outfit', sans-serif" }}
        >
          how lazybot hits different
        </motion.h2>

        <div className="space-y-8">
          {[
            {
              icon: Brain,
              title: "ai reads your resume like a recruiter",
              desc: "spots your skills. knows your worth. no cap."
            },
            {
              icon: Zap,
              title: "matches you with jobs that actually fit",
              desc: "analyzes jds. filters the noise. only shows you real ones."
            },
            {
              icon: Bot,
              title: "applies on your behalf. literally.",
              desc: "fills forms. uploads docs. hits submit. you do nothing."
            }
          ].map((item, i) => (
            <motion.div
              key={i}
              variants={fadeInUp}
              className="flex items-start gap-6 p-6 border border-[#E5E5E5] rounded-2xl hover:border-[#0A0A0A] transition-colors duration-300"
              data-testid={`solution-${i + 1}`}
            >
              <div className="w-12 h-12 bg-[#0A0A0A] rounded-full flex items-center justify-center flex-shrink-0">
                <item.icon className="w-5 h-5 text-[#FAFAFA]" />
              </div>
              <div>
                <h3 className="text-lg md:text-xl font-bold mb-1" style={{ fontFamily: "'Outfit', sans-serif" }}>
                  {item.title}
                </h3>
                <p className="text-sm text-[#888]" style={{ fontFamily: "'JetBrains Mono', monospace" }}>
                  {item.desc}
                </p>
              </div>
            </motion.div>
          ))}
        </div>
      </motion.div>
    </section>
  );
};

// Time Saved Section
const TimeSavedSection = () => {
  return (
    <section data-testid="time-section" className="py-24 md:py-32 px-6 md:px-12 lg:px-24 bg-[#FAFAFA]">
      <motion.div
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: "-100px" }}
        variants={staggerContainer}
        className="max-w-4xl"
      >
        <motion.h2
          variants={fadeInUp}
          className="text-3xl md:text-5xl lg:text-6xl font-black mb-8 leading-tight"
          style={{ fontFamily: "'Outfit', sans-serif" }}
        >
          what you get back:
          <br />
          <span className="text-[#888]">your life.</span>
        </motion.h2>

        <motion.div variants={fadeInUp} className="grid md:grid-cols-2 gap-6">
          <div className="bg-[#0A0A0A] text-[#FAFAFA] p-8 rounded-2xl">
            <p className="text-5xl md:text-6xl font-black mb-2" style={{ fontFamily: "'Outfit', sans-serif" }}>50</p>
            <p className="text-sm text-[#888]" style={{ fontFamily: "'JetBrains Mono', monospace" }}>applications per day</p>
          </div>
          <div className="bg-[#0A0A0A] text-[#FAFAFA] p-8 rounded-2xl">
            <p className="text-5xl md:text-6xl font-black mb-2" style={{ fontFamily: "'Outfit', sans-serif" }}>1,500</p>
            <p className="text-sm text-[#888]" style={{ fontFamily: "'JetBrains Mono', monospace" }}>applications per month</p>
          </div>
        </motion.div>

        <motion.p
          variants={fadeInUp}
          className="text-base text-[#888] mt-8"
          style={{ fontFamily: "'JetBrains Mono', monospace" }}
        >
          use the extra 200+ hours for interview prep. or touching grass. your call.
        </motion.p>
      </motion.div>
    </section>
  );
};

// Waitlist Section
const WaitlistSection = () => {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [loading, setLoading] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!name.trim() || !email.trim()) {
      toast.error("name and email required bestie");
      return;
    }
    setLoading(true);
    try {
      const response = await axios.post(`${API}/waitlist`, { name, email, phone: phone || null });
      if (response.data.success) {
        setSubmitted(true);
        toast.success("you're in! welcome to the lazy side");
      }
    } catch (error) {
      if (error.response?.status === 400) {
        toast.error("already on the list, chill");
      } else {
        toast.error("something broke. try again?");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <section id="waitlist" data-testid="waitlist-section" className="py-24 md:py-32 px-6 md:px-12 lg:px-24 bg-[#0A0A0A] text-[#FAFAFA]">
      <motion.div
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: "-100px" }}
        variants={staggerContainer}
        className="max-w-xl mx-auto text-center"
      >
        <motion.div
          variants={fadeInUp}
          className="inline-flex items-center gap-2 px-4 py-2 border border-[#333] rounded-full text-xs mb-8"
          style={{ fontFamily: "'JetBrains Mono', monospace" }}
        >
          <Gift className="w-3 h-3" />
          first 100 users get special perks
        </motion.div>

        <motion.h2
          variants={fadeInUp}
          className="text-3xl md:text-5xl lg:text-6xl font-black mb-4 leading-tight"
          style={{ fontFamily: "'Outfit', sans-serif" }}
        >
          be early.
          <br />
          be lazy.
          <br />
          <span className="text-[#888]">be hired.</span>
        </motion.h2>

        <motion.p
          variants={fadeInUp}
          className="text-sm text-[#888] mb-10"
          style={{ fontFamily: "'JetBrains Mono', monospace" }}
        >
          early birds get the best stuff. you know the drill.
        </motion.p>

        {!submitted ? (
          <motion.form variants={fadeInUp} onSubmit={handleSubmit} className="space-y-5 text-left">
            <input
              data-testid="waitlist-name-input"
              type="text"
              placeholder="your name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="input-inverted"
              disabled={loading}
            />
            <input
              data-testid="waitlist-email-input"
              type="email"
              placeholder="your email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="input-inverted"
              disabled={loading}
            />
            <input
              data-testid="waitlist-phone-input"
              type="tel"
              placeholder="phone (optional - for priority updates)"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              className="input-inverted"
              disabled={loading}
            />
            <button
              data-testid="waitlist-submit-btn"
              type="submit"
              disabled={loading}
              className="w-full py-4 bg-[#FAFAFA] text-[#0A0A0A] rounded-full font-semibold hover:bg-[#888] hover:text-[#FAFAFA] transition-colors duration-300 disabled:opacity-50"
              style={{ fontFamily: "'Outfit', sans-serif" }}
            >
              {loading ? "joining..." : "get early access"}
            </button>
          </motion.form>
        ) : (
          <motion.div initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }}>
            <div className="w-16 h-16 bg-[#FAFAFA] rounded-full flex items-center justify-center mx-auto mb-6">
              <Check className="w-8 h-8 text-[#0A0A0A]" />
            </div>
            <p className="text-xl font-bold mb-2" style={{ fontFamily: "'Outfit', sans-serif" }}>you're on the list!</p>
            <p className="text-sm text-[#888]" style={{ fontFamily: "'JetBrains Mono', monospace" }}>
              we'll hit you up when it's time. get ready to never fill forms again.
            </p>
          </motion.div>
        )}
      </motion.div>
    </section>
  );
};

// Contact Section
const ContactSection = () => {
  return (
    <section data-testid="contact-section" className="py-20 px-6 md:px-12 lg:px-24 bg-[#FAFAFA]">
      <motion.div
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: "-100px" }}
        variants={staggerContainer}
        className="max-w-4xl mx-auto text-center"
      >
        <motion.h3
          variants={fadeInUp}
          className="text-2xl md:text-3xl font-black mb-8"
          style={{ fontFamily: "'Outfit', sans-serif" }}
        >
          got questions? hit us up.
        </motion.h3>

        <motion.div variants={fadeInUp} className="flex flex-col md:flex-row justify-center items-center gap-8 md:gap-16">
          <a
            href="mailto:support@lazygen.site"
            className="text-sm text-[#666] hover:text-[#0A0A0A] transition-colors"
            style={{ fontFamily: "'JetBrains Mono', monospace" }}
            data-testid="contact-email"
          >
            support@lazygen.site
          </a>
          <div className="flex flex-col sm:flex-row gap-4 sm:gap-8">
            <a
              href="tel:+919718642745"
              className="text-sm text-[#666] hover:text-[#0A0A0A] transition-colors"
              style={{ fontFamily: "'JetBrains Mono', monospace" }}
              data-testid="contact-phone-1"
            >
              +91 97186 42745
            </a>
            <a
              href="tel:+916377406473"
              className="text-sm text-[#666] hover:text-[#0A0A0A] transition-colors"
              style={{ fontFamily: "'JetBrains Mono', monospace" }}
              data-testid="contact-phone-2"
            >
              +91 6377406473
            </a>
          </div>
        </motion.div>
      </motion.div>
    </section>
  );
};

// Footer
const Footer = () => {
  return (
    <footer data-testid="footer-section" className="py-12 px-6 md:px-12 lg:px-24 border-t border-[#E5E5E5]">
      <div className="max-w-5xl mx-auto flex flex-col md:flex-row justify-between items-center gap-6">
        <div className="flex items-center gap-3">
          <img src={PANDA_LOGO} alt="LazyBot" className="w-10 h-10 object-contain" />
          <span className="text-lg font-bold" style={{ fontFamily: "'Outfit', sans-serif" }}>LazyBot</span>
        </div>
        <p className="text-xs text-[#888]" style={{ fontFamily: "'JetBrains Mono', monospace" }}>
          © 2025 LazyGen · built for lazy geniuses
        </p>
      </div>
    </footer>
  );
};

function App() {
  return (
    <div className="App relative">
      <div className="noise-overlay" />
      <Toaster
        position="bottom-right"
        toastOptions={{
          style: {
            background: '#0A0A0A',
            color: '#FAFAFA',
            fontFamily: "'JetBrains Mono', monospace",
            border: '1px solid #222'
          }
        }}
      />
      <HeroSection />
      <StruggleSection />
      <SolutionSection />
      <TimeSavedSection />
      <WaitlistSection />
      <ContactSection />
      <Footer />
    </div>
  );
}

export default App;
