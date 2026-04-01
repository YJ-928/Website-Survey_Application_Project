import React, { useState, useEffect } from 'react';
import { Navbar, Container } from 'react-bootstrap';
import { useNavigate, useLocation } from 'react-router-dom';
import { useLanguage } from '../../context/LanguageContext';

const AppNavbar: React.FC = () => {
  const [expanded, setExpanded] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();
  const { language, setLanguage, toggleLanguage } = useLanguage();

  // Show language switcher ONLY on survey page
  const showLanguageSwitcher = location.pathname === '/';

  // Auto-reset to English when navigating away from survey page
  useEffect(() => {
    if (!showLanguageSwitcher && language === 'te') {
      setLanguage('en');
    }
  }, [location.pathname, showLanguageSwitcher, language, setLanguage]);

  const handleBrandClick = () => {
    navigate('/');
    setExpanded(false);
  };

  return (
    <Navbar
      expanded={expanded}
      onToggle={setExpanded}
      expand="lg"
      bg="light"
      variant="light"
      className="navbar-custom"
    >
      <Container fluid className="px-3 px-md-4 px-sm-2">
        <Navbar.Brand
          as="div"
          onClick={handleBrandClick}
          className="d-flex align-items-center"
          style={{ cursor: 'pointer' }}
        >
          <span className="navbar-title fw-bold">
            {showLanguageSwitcher && language === 'te' ? 'సర్వే అప్లికేషన్' : 'Survey Application'}
          </span>
        </Navbar.Brand>

        {/* Language Toggle Switch */}
        {showLanguageSwitcher && (
          <div className="language-switch ms-auto">
            <input 
              id="language-toggle" 
              type="checkbox" 
              checked={language === 'te'}
              onChange={toggleLanguage}
            />
            <label htmlFor="language-toggle" className="language-slider">
              <span className="language-label en">EN</span>
              <span className="language-label te">తె</span>
            </label>
          </div>
        )}

        {/* <Navbar.Toggle aria-controls="basic-navbar-nav" />                 */}
        {/* <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="ms-auto">
            <Nav.Link
              as={Link}
              to="/"
              onClick={() => setExpanded(false)}
              className="nav-link-custom"
            >
              Survey
            </Nav.Link>
            <Nav.Link
              onClick={handleLoginClick}
              className="nav-link-custom btn-login"
            >
              <i className="bi bi-person-circle me-2"></i>
              Admin Login
            </Nav.Link>
          </Nav>
        </Navbar.Collapse> */}
      </Container>
    </Navbar>
  );
};

export default AppNavbar;
