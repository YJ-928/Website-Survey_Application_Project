-- =====================================================
-- WOMEN EMPOWERMENT SURVEY - PostgreSQL DATABASE DESIGN
-- NALGONDA DISTRICT, TELANGANA
-- =====================================================
-- Author: Senior Solution Architect
-- Version: 2.0
-- Description: Complete database schema for Women Empowerment 
--              Survey Application - Nalgonda District Specific
-- Location Hierarchy: District → Revenue Division → Mandal → Village/Area (input)
-- =====================================================

-- Enable UUID extension for unique identifiers
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- =====================================================
-- SECTION 1: LOCATION MASTER TABLES (NALGONDA SPECIFIC)
-- =====================================================

-- 1.1 District Master (Single record for Nalgonda)
CREATE TABLE districts (
    district_id SERIAL PRIMARY KEY,
    district_code VARCHAR(10) UNIQUE NOT NULL,
    district_name VARCHAR(100) NOT NULL,
    state_code VARCHAR(10) NOT NULL DEFAULT 'TS',
    state_name VARCHAR(100) NOT NULL DEFAULT 'Telangana',
    district_hq VARCHAR(100),
    total_revenue_divisions INTEGER,
    total_mandals INTEGER,
    total_municipalities INTEGER,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE districts IS 'District master - Currently configured for Nalgonda, Telangana';

-- Insert Nalgonda District
INSERT INTO districts (district_code, district_name, state_code, state_name, district_hq, total_revenue_divisions, total_mandals, total_municipalities) 
VALUES ('NLG', 'Nalgonda', 'TS', 'Telangana', 'Nalgonda', 3, 31, 3);

-- 1.2 Revenue Divisions (Dropdown - Level 1)
CREATE TABLE revenue_divisions (
    division_id SERIAL PRIMARY KEY,
    division_code VARCHAR(20) UNIQUE NOT NULL,
    division_name VARCHAR(100) NOT NULL,
    district_id INTEGER NOT NULL REFERENCES districts(district_id),
    division_hq VARCHAR(100),
    total_mandals INTEGER,
    display_order INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_revenue_divisions_district ON revenue_divisions(district_id);

COMMENT ON TABLE revenue_divisions IS 'Revenue Divisions within Nalgonda district (Dropdown selection)';

-- Insert 3 Revenue Divisions of Nalgonda
INSERT INTO revenue_divisions (division_code, division_name, district_id, division_hq, total_mandals, display_order) VALUES
('NLG-NLG', 'Nalgonda', 1, 'Nalgonda', 11, 1),
('NLG-MRY', 'Miryalaguda', 1, 'Miryalaguda', 10, 2),
('NLG-DVK', 'Devarakonda', 1, 'Devarakonda', 10, 3);

-- 1.3 Mandals (Dropdown - Level 2, dependent on Revenue Division)
CREATE TABLE mandals (
    mandal_id SERIAL PRIMARY KEY,
    mandal_code VARCHAR(20) UNIQUE NOT NULL,
    mandal_name VARCHAR(150) NOT NULL,
    local_name VARCHAR(150), -- Telugu/local name if different
    division_id INTEGER NOT NULL REFERENCES revenue_divisions(division_id),
    district_id INTEGER NOT NULL REFERENCES districts(district_id),
    is_municipality BOOLEAN DEFAULT FALSE,
    population INTEGER,
    area_sq_km DECIMAL(10,2),
    display_order INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_mandals_division ON mandals(division_id);
CREATE INDEX idx_mandals_district ON mandals(district_id);
CREATE INDEX idx_mandals_municipality ON mandals(is_municipality);

COMMENT ON TABLE mandals IS 'Mandals within each Revenue Division (Dropdown selection - cascaded from Revenue Division)';

-- Insert all 31 Mandals of Nalgonda District

-- Nalgonda Revenue Division (11 Mandals)
INSERT INTO mandals (mandal_code, mandal_name, local_name, division_id, district_id, display_order) VALUES
('NLG-001', 'Nalgonda', NULL, 1, 1, 1),
('NLG-002', 'Nakrekal', NULL, 1, 1, 2),
('NLG-003', 'Narketpally', NULL, 1, 1, 3),
('NLG-004', 'Chandur', NULL, 1, 1, 4),
('NLG-005', 'Munugode', NULL, 1, 1, 5),
('NLG-006', 'Kattangur', NULL, 1, 1, 6),
('NLG-007', 'Kanagal', NULL, 1, 1, 7),
('NLG-008', 'Chityal', NULL, 1, 1, 8),
('NLG-009', 'Thipparthy', NULL, 1, 1, 9),
('NLG-010', 'Narayanpur', 'Samsthan Narayanapur', 1, 1, 10),
('NLG-011', 'Kethepally', NULL, 1, 1, 11);

-- Miryalaguda Revenue Division (10 Mandals)
INSERT INTO mandals (mandal_code, mandal_name, local_name, division_id, district_id, display_order) VALUES
('MRY-001', 'Miryalaguda', NULL, 2, 1, 1),
('MRY-002', 'Vemulapally', NULL, 2, 1, 2),
('MRY-003', 'Nidmanoor', NULL, 2, 1, 3),
('MRY-004', 'Tripuraram', NULL, 2, 1, 4),
('MRY-005', 'Anumula', 'Haliya', 2, 1, 5),
('MRY-006', 'Dameracherla', NULL, 2, 1, 6),
('MRY-007', 'Peddavoora', NULL, 2, 1, 7),
('MRY-008', 'Shaligouraram', NULL, 2, 1, 8),
('MRY-009', 'Adavidevulapally', NULL, 2, 1, 9),
('MRY-010', 'Nampally', NULL, 2, 1, 10);

-- Devarakonda Revenue Division (10 Mandals)
INSERT INTO mandals (mandal_code, mandal_name, local_name, division_id, district_id, display_order) VALUES
('DVK-001', 'Devarakonda', NULL, 3, 1, 1),
('DVK-002', 'Marriguda', NULL, 3, 1, 2),
('DVK-003', 'Pedda Adiserla Pally', 'P.A. Palli', 3, 1, 3),
('DVK-004', 'M. Turkapally', NULL, 3, 1, 4),
('DVK-005', 'Chandampet', NULL, 3, 1, 5),
('DVK-006', 'Gurrampod', NULL, 3, 1, 6),
('DVK-007', 'Neredcherla', NULL, 3, 1, 7),
('DVK-008', 'Perur', 'Perka Kondaram', 3, 1, 8),
('DVK-009', 'Mattampally', NULL, 3, 1, 9),
('DVK-010', 'Ananthagiri', NULL, 3, 1, 10);

-- 1.4 Municipalities (Reference table)
CREATE TABLE municipalities (
    municipality_id SERIAL PRIMARY KEY,
    municipality_code VARCHAR(20) UNIQUE NOT NULL,
    municipality_name VARCHAR(150) NOT NULL,
    municipality_type VARCHAR(50) DEFAULT 'Municipality', -- Municipality, Municipal Corporation, Nagar Panchayat
    division_id INTEGER NOT NULL REFERENCES revenue_divisions(division_id),
    district_id INTEGER NOT NULL REFERENCES districts(district_id),
    is_district_hq BOOLEAN DEFAULT FALSE,
    population INTEGER,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE municipalities IS 'Municipalities in Nalgonda district for reference';

-- Insert 3 Municipalities
INSERT INTO municipalities (municipality_code, municipality_name, division_id, district_id, is_district_hq) VALUES
('MUN-NLG', 'Nalgonda', 1, 1, TRUE),
('MUN-MRY', 'Miryalaguda', 2, 1, FALSE),
('MUN-DVK', 'Devarakonda', 3, 1, FALSE);

-- 1.5 Area Types (for Rural/Urban classification)
CREATE TABLE area_types (
    area_type_id SERIAL PRIMARY KEY,
    type_code VARCHAR(20) UNIQUE NOT NULL,
    type_name VARCHAR(50) NOT NULL,
    description TEXT,
    display_order INTEGER DEFAULT 0
);

INSERT INTO area_types (type_code, type_name, description, display_order) VALUES
('RURAL', 'Rural', 'Village/Rural area', 1),
('URBAN', 'Urban', 'Municipal/Town area', 2),
('SEMI_URBAN', 'Semi-Urban', 'Peri-urban/Semi-urban area', 3);

-- =====================================================
-- SECTION 2: OTHER MASTER/LOOKUP TABLES
-- =====================================================

-- 2.1 Age Groups Lookup
CREATE TABLE age_groups (
    age_group_id SERIAL PRIMARY KEY,
    age_range VARCHAR(20) NOT NULL UNIQUE,
    min_age INTEGER NOT NULL,
    max_age INTEGER NOT NULL,
    display_order INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE
);

INSERT INTO age_groups (age_range, min_age, max_age, display_order) VALUES
('18-25', 18, 25, 1),
('26-30', 26, 30, 2),
('31-35', 31, 35, 3),
('36-40', 36, 40, 4),
('40+', 41, 100, 5);

-- 2.2 User Status Types
CREATE TABLE user_status_types (
    status_id SERIAL PRIMARY KEY,
    status_code VARCHAR(30) NOT NULL UNIQUE,
    status_name VARCHAR(50) NOT NULL,
    status_name_telugu VARCHAR(100), -- Telugu translation
    description TEXT,
    display_order INTEGER DEFAULT 0,
    requires_additional_info BOOLEAN DEFAULT FALSE,
    next_flow_step VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE
);

INSERT INTO user_status_types (status_code, status_name, status_name_telugu, description, display_order, requires_additional_info, next_flow_step) VALUES
('HOMEMAKER', 'Homemaker', 'గృహిణి', 'Primary homemaker/housewife', 1, TRUE, 'income_activity'),
('STUDENT', 'Student', 'విద్యార్థి', 'Currently pursuing education', 2, FALSE, 'goals'),
('EMPLOYED', 'Employed', 'ఉద్యోగి', 'Currently employed', 3, FALSE, 'goals'),
('ENTREPRENEUR_ASPIRING', 'Aspiring Entrepreneur', 'ఆకాంక్షిస్తున్న వ్యాపారవేత్త', 'Wants to start a business', 4, TRUE, 'aspiring_entrepreneur'),
('ENTREPRENEUR_EXISTING', 'Existing Entrepreneur', 'ప్రస్తుత వ్యాపారవేత్త', 'Already running a business', 5, TRUE, 'existing_entrepreneur'),
('FARMER', 'Farmer', 'రైతు', 'Engaged in agricultural activities', 6, TRUE, 'farmer'),
('DIFFERENTLY_ABLED', 'Differently-Abled', 'వికలాంగులు', 'Person with disabilities', 7, TRUE, 'differently_abled'),
('UNEMPLOYED', 'Unemployed', 'నిరుద్యోగి', 'Currently not employed', 8, FALSE, 'goals');

-- 2.3 Interest Types (for income activities)
CREATE TABLE interest_types (
    interest_id SERIAL PRIMARY KEY,
    interest_code VARCHAR(30) NOT NULL UNIQUE,
    interest_name VARCHAR(100) NOT NULL,
    interest_name_telugu VARCHAR(150),
    category VARCHAR(50),
    display_order INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE
);

INSERT INTO interest_types (interest_code, interest_name, interest_name_telugu, category, display_order) VALUES
('TAILORING', 'Tailoring', 'టైలరింగ్', 'Skills', 1),
('FOOD', 'Food Business', 'ఆహార వ్యాపారం', 'Business', 2),
('HANDICRAFTS', 'Handicrafts', 'హస్తకళలు', 'Skills', 3),
('BEAUTY', 'Beauty Services', 'అందం సేవలు', 'Services', 4),
('ONLINE_SELLING', 'Online Selling', 'ఆన్‌లైన్ అమ్మకాలు', 'Digital', 5);

-- 2.4 Support Types (General)
CREATE TABLE support_types (
    support_id SERIAL PRIMARY KEY,
    support_code VARCHAR(30) NOT NULL UNIQUE,
    support_name VARCHAR(100) NOT NULL,
    support_name_telugu VARCHAR(150),
    category VARCHAR(50),
    display_order INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE
);

INSERT INTO support_types (support_code, support_name, support_name_telugu, category, display_order) VALUES
('TRAINING', 'Training', 'శిక్షణ', 'Capacity Building', 1),
('FUNDING', 'Funding/Loan', 'నిధులు/రుణం', 'Financial', 2),
('EQUIPMENT', 'Equipment', 'పరికరాలు', 'Infrastructure', 3),
('MARKET_ACCESS', 'Market Access', 'మార్కెట్ యాక్సెస్', 'Business', 4),
('GOVT_SCHEME', 'Government Scheme Support', 'ప్రభుత్వ పథక మద్దతు', 'Policy', 5),
('SUBSIDY', 'Subsidy', 'సబ్సిడీ', 'Financial', 6),
('LAND', 'Land', 'భూమి', 'Infrastructure', 7);

-- 2.5 Business Types (for entrepreneurs)
CREATE TABLE business_types (
    business_type_id SERIAL PRIMARY KEY,
    type_code VARCHAR(30) NOT NULL UNIQUE,
    type_name VARCHAR(100) NOT NULL,
    type_name_telugu VARCHAR(150),
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE
);

INSERT INTO business_types (type_code, type_name, type_name_telugu) VALUES
('RETAIL', 'Retail/Shop', 'రిటైల్/షాప్'),
('SERVICES', 'Services', 'సేవలు'),
('MANUFACTURING', 'Manufacturing', 'తయారీ'),
('FOOD_BEVERAGES', 'Food & Beverages', 'ఆహారం & పానీయాలు'),
('TEXTILES', 'Textiles/Garments', 'వస్త్రాలు/దుస్తులు'),
('HANDICRAFTS', 'Handicrafts/Artisan', 'హస్తకళలు/కళాకారులు'),
('AGRICULTURE', 'Agriculture-based', 'వ్యవసాయ ఆధారిత'),
('TECHNOLOGY', 'Technology/Digital', 'టెక్నాలజీ/డిజిటల్'),
('OTHER', 'Other', 'ఇతర');

-- 2.6 Business Scale Types
CREATE TABLE business_scales (
    scale_id SERIAL PRIMARY KEY,
    scale_code VARCHAR(20) NOT NULL UNIQUE,
    scale_name VARCHAR(50) NOT NULL,
    scale_name_telugu VARCHAR(100),
    description TEXT,
    display_order INTEGER DEFAULT 0
);

INSERT INTO business_scales (scale_code, scale_name, scale_name_telugu, description, display_order) VALUES
('HOME_BASED', 'Home-based', 'ఇంటి ఆధారిత', 'Business operated from home', 1),
('MICRO', 'Micro', 'మైక్రో', 'Micro enterprise', 2),
('SMALL', 'Small', 'చిన్న', 'Small enterprise', 3),
('LARGE', 'Large', 'పెద్ద', 'Large enterprise', 4);

-- 2.7 Business Challenge Types
CREATE TABLE challenge_types (
    challenge_id SERIAL PRIMARY KEY,
    challenge_code VARCHAR(30) NOT NULL UNIQUE,
    challenge_name VARCHAR(100) NOT NULL,
    challenge_name_telugu VARCHAR(150),
    display_order INTEGER DEFAULT 0
);

INSERT INTO challenge_types (challenge_code, challenge_name, challenge_name_telugu, display_order) VALUES
('FINANCE', 'Finance/Capital', 'ఆర్థిక/మూలధనం', 1),
('MARKETING', 'Marketing', 'మార్కెటింగ్', 2),
('SKILLS', 'Skills Gap', 'నైపుణ్యాల లోపం', 3),
('RAW_MATERIAL', 'Raw Material Access', 'ముడి పదార్థాల ప్రాప్యత', 4),
('LABOR', 'Labor/Workforce', 'శ్రామికులు', 5),
('TECHNOLOGY', 'Technology', 'సాంకేతికత', 6);

-- 2.8 Improvement/Growth Goals
CREATE TABLE improvement_goals (
    goal_id SERIAL PRIMARY KEY,
    goal_code VARCHAR(30) NOT NULL UNIQUE,
    goal_name VARCHAR(100) NOT NULL,
    goal_name_telugu VARCHAR(150),
    goal_category VARCHAR(50),
    display_order INTEGER DEFAULT 0
);

INSERT INTO improvement_goals (goal_code, goal_name, goal_name_telugu, goal_category, display_order) VALUES
('INCREASE_INCOME', 'Increase Income', 'ఆదాయం పెంచుకోవడం', 'Growth', 1),
('EXPAND_MARKET', 'Expand Market', 'మార్కెట్ విస్తరణ', 'Growth', 2),
('DIGITIZE', 'Digitize Business', 'వ్యాపారాన్ని డిజిటల్ చేయడం', 'Technology', 3),
('GET_TRAINED', 'Get Training', 'శిక్షణ పొందడం', 'Capacity', 4),
('GET_JOB', 'Get Employment', 'ఉద్యోగం పొందడం', 'Employment', 5),
('START_BUSINESS', 'Start Business', 'వ్యాపారం ప్రారంభించడం', 'Entrepreneurship', 6);

-- 2.9 Work Modes (for differently-abled)
CREATE TABLE work_modes (
    work_mode_id SERIAL PRIMARY KEY,
    mode_code VARCHAR(20) NOT NULL UNIQUE,
    mode_name VARCHAR(50) NOT NULL,
    mode_name_telugu VARCHAR(100),
    display_order INTEGER DEFAULT 0
);

INSERT INTO work_modes (mode_code, mode_name, mode_name_telugu, display_order) VALUES
('HOME', 'Home-based Work', 'ఇంటి ఆధారిత పని', 1),
('OFFICE', 'Office/Workplace', 'కార్యాలయం', 2),
('DIGITAL', 'Digital/Remote', 'డిజిటల్/రిమోట్', 3),
('HYBRID', 'Hybrid', 'హైబ్రిడ్', 4);

-- 2.10 Differently-Abled Support Types
CREATE TABLE differently_abled_support_types (
    da_support_id SERIAL PRIMARY KEY,
    support_code VARCHAR(30) NOT NULL UNIQUE,
    support_name VARCHAR(100) NOT NULL,
    support_name_telugu VARCHAR(150),
    display_order INTEGER DEFAULT 0
);

INSERT INTO differently_abled_support_types (support_code, support_name, support_name_telugu, display_order) VALUES
('ASSISTIVE_DEVICES', 'Assistive Devices', 'సహాయక పరికరాలు', 1),
('HOME_WORK', 'Home-based Work', 'ఇంటి ఆధారిత పని', 2),
('FLEXIBLE_HOURS', 'Flexible Hours', 'సౌలభ్య సమయాలు', 3),
('TRAINING', 'Specialized Training', 'ప్రత్యేక శిక్షణ', 4);

-- 2.11 Agriculture Interest Types
CREATE TABLE agri_interest_types (
    agri_interest_id SERIAL PRIMARY KEY,
    interest_code VARCHAR(30) NOT NULL UNIQUE,
    interest_name VARCHAR(100) NOT NULL,
    interest_name_telugu VARCHAR(150),
    display_order INTEGER DEFAULT 0
);

INSERT INTO agri_interest_types (interest_code, interest_name, interest_name_telugu, display_order) VALUES
('CROP', 'Crop Farming', 'పంట సాగు', 1),
('DAIRY', 'Dairy', 'పాడి పరిశ్రమ', 2),
('POULTRY', 'Poultry', 'కోళ్ల పెంపకం', 3),
('FISHERY', 'Fisheries', 'చేపల పెంపకం', 4);

-- 2.12 Agriculture Support Types
CREATE TABLE agri_support_types (
    agri_support_id SERIAL PRIMARY KEY,
    support_code VARCHAR(30) NOT NULL UNIQUE,
    support_name VARCHAR(100) NOT NULL,
    support_name_telugu VARCHAR(150),
    display_order INTEGER DEFAULT 0
);

INSERT INTO agri_support_types (support_code, support_name, support_name_telugu, display_order) VALUES
('FARM_IMPLEMENTS', 'Farm Implements', 'వ్యవసాయ పరికరాలు', 1),
('TRAINING', 'Agricultural Training', 'వ్యవసాయ శిక్షణ', 2),
('SUBSIDY', 'Subsidy', 'సబ్సిడీ', 3),
('MARKET_ACCESS', 'Market Access', 'మార్కెట్ యాక్సెస్', 4);

-- 2.13 Land Purpose Types
CREATE TABLE land_purposes (
    purpose_id SERIAL PRIMARY KEY,
    purpose_code VARCHAR(30) NOT NULL UNIQUE,
    purpose_name VARCHAR(100) NOT NULL,
    purpose_name_telugu VARCHAR(150),
    display_order INTEGER DEFAULT 0
);

INSERT INTO land_purposes (purpose_code, purpose_name, purpose_name_telugu, display_order) VALUES
('HOUSING', 'Housing', 'గృహ నిర్మాణం', 1),
('BUSINESS', 'Business', 'వ్యాపారం', 2),
('FARMING', 'Farming', 'వ్యవసాయం', 3);

-- 2.14 Land Support Types
CREATE TABLE land_support_types (
    land_support_id SERIAL PRIMARY KEY,
    support_code VARCHAR(30) NOT NULL UNIQUE,
    support_name VARCHAR(100) NOT NULL,
    support_name_telugu VARCHAR(150),
    display_order INTEGER DEFAULT 0
);

INSERT INTO land_support_types (support_code, support_name, support_name_telugu, display_order) VALUES
('OWNERSHIP', 'Ownership', 'యాజమాన్యం', 1),
('LEASE', 'Lease', 'లీజు', 2),
('SCHEME_ASSISTANCE', 'Scheme Assistance', 'పథక సహాయం', 3);

-- 2.15 Time Horizons
CREATE TABLE time_horizons (
    horizon_id SERIAL PRIMARY KEY,
    horizon_code VARCHAR(20) NOT NULL UNIQUE,
    horizon_name VARCHAR(50) NOT NULL,
    horizon_name_telugu VARCHAR(100),
    min_years DECIMAL(3,1),
    max_years DECIMAL(3,1),
    display_order INTEGER DEFAULT 0
);

INSERT INTO time_horizons (horizon_code, horizon_name, horizon_name_telugu, min_years, max_years, display_order) VALUES
('SHORT_TERM', 'Short-Term (0-1 year)', 'స్వల్పకాలిక (0-1 సంవత్సరం)', 0, 1, 1),
('MEDIUM_TERM', 'Medium-Term (1-3 years)', 'మధ్యకాలిక (1-3 సంవత్సరాలు)', 1, 3, 2),
('LONG_TERM', 'Long-Term (3-5 years)', 'దీర్ఘకాలిక (3-5 సంవత్సరాలు)', 3, 5, 3);

-- 2.16 Goal Types (for time horizons)
CREATE TABLE goal_types (
    goal_type_id SERIAL PRIMARY KEY,
    goal_code VARCHAR(30) NOT NULL UNIQUE,
    goal_name VARCHAR(100) NOT NULL,
    goal_name_telugu VARCHAR(150),
    applicable_horizons TEXT[],
    display_order INTEGER DEFAULT 0
);

INSERT INTO goal_types (goal_code, goal_name, goal_name_telugu, applicable_horizons, display_order) VALUES
('TRAINING', 'Training', 'శిక్షణ', ARRAY['SHORT_TERM'], 1),
('INCOME', 'Income Generation', 'ఆదాయ ఉత్పత్తి', ARRAY['SHORT_TERM'], 2),
('JOB', 'Employment', 'ఉద్యోగం', ARRAY['SHORT_TERM'], 3),
('BUSINESS', 'Start Business', 'వ్యాపారం ప్రారంభం', ARRAY['MEDIUM_TERM'], 4),
('STABILITY', 'Financial Stability', 'ఆర్థిక స్థిరత్వం', ARRAY['MEDIUM_TERM'], 5),
('EXPANSION', 'Business Expansion', 'వ్యాపార విస్తరణ', ARRAY['LONG_TERM'], 6),
('EDUCATION', 'Higher Education', 'ఉన్నత విద్య', ARRAY['LONG_TERM'], 7);

-- =====================================================
-- SECTION 3: ADMIN/AUTHENTICATION TABLES
-- =====================================================

-- 3.1 Admin Users
CREATE TABLE admin_users (
    admin_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(150) NOT NULL,
    role VARCHAR(50) DEFAULT 'admin' CHECK (role IN ('super_admin', 'admin', 'viewer')),
    department VARCHAR(100),
    designation VARCHAR(100),
    phone VARCHAR(20),
    assigned_division_id INTEGER REFERENCES revenue_divisions(division_id), -- Optional: Restrict to specific division
    is_active BOOLEAN DEFAULT TRUE,
    is_email_verified BOOLEAN DEFAULT FALSE,
    last_login_at TIMESTAMP WITH TIME ZONE,
    failed_login_attempts INTEGER DEFAULT 0,
    locked_until TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by UUID REFERENCES admin_users(admin_id)
);

CREATE INDEX idx_admin_email ON admin_users(email);
CREATE INDEX idx_admin_active ON admin_users(is_active);
CREATE INDEX idx_admin_division ON admin_users(assigned_division_id);

COMMENT ON TABLE admin_users IS 'Admin users who can access the dashboard with authentication';

-- 3.2 Admin Sessions
CREATE TABLE admin_sessions (
    session_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    admin_id UUID NOT NULL REFERENCES admin_users(admin_id) ON DELETE CASCADE,
    token_hash VARCHAR(255) NOT NULL,
    ip_address INET,
    user_agent TEXT,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    is_revoked BOOLEAN DEFAULT FALSE
);

CREATE INDEX idx_session_admin ON admin_sessions(admin_id);
CREATE INDEX idx_session_token ON admin_sessions(token_hash);
CREATE INDEX idx_session_expires ON admin_sessions(expires_at);

-- 3.3 Password Reset Tokens
CREATE TABLE password_reset_tokens (
    token_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    admin_id UUID NOT NULL REFERENCES admin_users(admin_id) ON DELETE CASCADE,
    token_hash VARCHAR(255) NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    used_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3.4 Admin Audit Log
CREATE TABLE admin_audit_log (
    audit_id BIGSERIAL PRIMARY KEY,
    admin_id UUID REFERENCES admin_users(admin_id),
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(50),
    entity_id VARCHAR(100),
    old_values JSONB,
    new_values JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_audit_admin ON admin_audit_log(admin_id);
CREATE INDEX idx_audit_action ON admin_audit_log(action);
CREATE INDEX idx_audit_created ON admin_audit_log(created_at);

-- =====================================================
-- SECTION 4: SURVEY RESPONSE TABLES
-- =====================================================

-- 4.1 Main Survey Responses Table
CREATE TABLE survey_responses (
    response_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    reference_id VARCHAR(20) NOT NULL UNIQUE, -- Format: WE-NLG-XXXXXX
    
    -- Location Information (Nalgonda Specific Hierarchy)
    district_id INTEGER NOT NULL DEFAULT 1 REFERENCES districts(district_id), -- Fixed to Nalgonda
    division_id INTEGER NOT NULL REFERENCES revenue_divisions(division_id), -- Dropdown
    mandal_id INTEGER NOT NULL REFERENCES mandals(mandal_id), -- Dropdown (cascaded from division)
    village_area_name VARCHAR(200) NOT NULL, -- FREE TEXT INPUT FIELD
    area_type_id INTEGER REFERENCES area_types(area_type_id), -- Rural/Urban/Semi-Urban
    
    -- Demographic Information
    age_group_id INTEGER NOT NULL REFERENCES age_groups(age_group_id),
    user_status_id INTEGER NOT NULL REFERENCES user_status_types(status_id),
    
    -- Income Activity Interest (for homemakers/unemployed)
    wants_income_activity BOOLEAN,
    
    -- Entrepreneur Status (if entrepreneur)
    entrepreneur_stage VARCHAR(20) CHECK (entrepreneur_stage IN ('ASPIRING', 'EXISTING', 'GROWTH')),
    
    -- Land Requirement
    requires_land BOOLEAN DEFAULT FALSE,
    
    -- Submission Info
    submission_mode VARCHAR(20) NOT NULL CHECK (submission_mode IN ('ONLINE', 'OFFLINE')),
    submission_device VARCHAR(50),
    ip_address INET,
    
    -- Timestamps
    started_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Status
    is_complete BOOLEAN DEFAULT FALSE,
    current_step INTEGER DEFAULT 1
);

-- Indexes for common queries and dashboard aggregations
CREATE INDEX idx_response_district ON survey_responses(district_id);
CREATE INDEX idx_response_division ON survey_responses(division_id);
CREATE INDEX idx_response_mandal ON survey_responses(mandal_id);
CREATE INDEX idx_response_age ON survey_responses(age_group_id);
CREATE INDEX idx_response_status ON survey_responses(user_status_id);
CREATE INDEX idx_response_area_type ON survey_responses(area_type_id);
CREATE INDEX idx_response_submission_mode ON survey_responses(submission_mode);
CREATE INDEX idx_response_created ON survey_responses(created_at);
CREATE INDEX idx_response_complete ON survey_responses(is_complete);
CREATE INDEX idx_response_entrepreneur_stage ON survey_responses(entrepreneur_stage) WHERE entrepreneur_stage IS NOT NULL;
CREATE INDEX idx_response_reference ON survey_responses(reference_id);
CREATE INDEX idx_response_village ON survey_responses(village_area_name); -- For searching by village name

COMMENT ON TABLE survey_responses IS 'Main table storing all survey responses from Nalgonda district';
COMMENT ON COLUMN survey_responses.reference_id IS 'User-friendly reference ID (e.g., WE-NLG-A93F2X)';
COMMENT ON COLUMN survey_responses.village_area_name IS 'Free text input for village or area name';

-- 4.2 Survey Interests (Many-to-Many)
CREATE TABLE survey_interests (
    survey_interest_id BIGSERIAL PRIMARY KEY,
    response_id UUID NOT NULL REFERENCES survey_responses(response_id) ON DELETE CASCADE,
    interest_id INTEGER NOT NULL REFERENCES interest_types(interest_id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(response_id, interest_id)
);

CREATE INDEX idx_survey_interests_response ON survey_interests(response_id);
CREATE INDEX idx_survey_interests_interest ON survey_interests(interest_id);

-- 4.3 Survey Support Needs (Many-to-Many)
CREATE TABLE survey_support_needs (
    survey_support_id BIGSERIAL PRIMARY KEY,
    response_id UUID NOT NULL REFERENCES survey_responses(response_id) ON DELETE CASCADE,
    support_id INTEGER NOT NULL REFERENCES support_types(support_id),
    priority INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(response_id, support_id)
);

CREATE INDEX idx_survey_support_response ON survey_support_needs(response_id);
CREATE INDEX idx_survey_support_type ON survey_support_needs(support_id);

-- =====================================================
-- SECTION 5: ENTREPRENEUR-SPECIFIC TABLES
-- =====================================================

-- 5.1 Entrepreneur Details
CREATE TABLE entrepreneur_details (
    entrepreneur_id BIGSERIAL PRIMARY KEY,
    response_id UUID NOT NULL UNIQUE REFERENCES survey_responses(response_id) ON DELETE CASCADE,
    
    -- Aspiring Entrepreneur Fields
    business_type_id INTEGER REFERENCES business_types(business_type_id),
    preferred_scale_id INTEGER REFERENCES business_scales(scale_id),
    
    -- Existing Entrepreneur Fields
    business_category VARCHAR(100),
    years_in_operation INTEGER,
    annual_revenue_range VARCHAR(50),
    employee_count INTEGER,
    
    -- Common Fields
    has_business_registration BOOLEAN,
    has_bank_account BOOLEAN,
    uses_digital_payments BOOLEAN,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_entrepreneur_response ON entrepreneur_details(response_id);
CREATE INDEX idx_entrepreneur_type ON entrepreneur_details(business_type_id);

-- 5.2 Entrepreneur Challenges (Many-to-Many)
CREATE TABLE entrepreneur_challenges (
    ec_id BIGSERIAL PRIMARY KEY,
    response_id UUID NOT NULL REFERENCES survey_responses(response_id) ON DELETE CASCADE,
    challenge_id INTEGER NOT NULL REFERENCES challenge_types(challenge_id),
    severity INTEGER CHECK (severity BETWEEN 1 AND 5),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(response_id, challenge_id)
);

CREATE INDEX idx_ent_challenges_response ON entrepreneur_challenges(response_id);
CREATE INDEX idx_ent_challenges_type ON entrepreneur_challenges(challenge_id);

-- 5.3 Entrepreneur Improvement Goals (Many-to-Many)
CREATE TABLE entrepreneur_improvement_goals (
    eig_id BIGSERIAL PRIMARY KEY,
    response_id UUID NOT NULL REFERENCES survey_responses(response_id) ON DELETE CASCADE,
    goal_id INTEGER NOT NULL REFERENCES improvement_goals(goal_id),
    priority INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(response_id, goal_id)
);

CREATE INDEX idx_ent_goals_response ON entrepreneur_improvement_goals(response_id);
CREATE INDEX idx_ent_goals_type ON entrepreneur_improvement_goals(goal_id);

-- =====================================================
-- SECTION 6: DIFFERENTLY-ABLED SPECIFIC TABLES
-- =====================================================

-- 6.1 Differently-Abled Details
CREATE TABLE differently_abled_details (
    da_detail_id BIGSERIAL PRIMARY KEY,
    response_id UUID NOT NULL UNIQUE REFERENCES survey_responses(response_id) ON DELETE CASCADE,
    disability_type VARCHAR(100),
    preferred_work_mode_id INTEGER REFERENCES work_modes(work_mode_id),
    additional_requirements TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_da_response ON differently_abled_details(response_id);

-- 6.2 Differently-Abled Support Needs (Many-to-Many)
CREATE TABLE differently_abled_support_needs (
    dasn_id BIGSERIAL PRIMARY KEY,
    response_id UUID NOT NULL REFERENCES survey_responses(response_id) ON DELETE CASCADE,
    da_support_id INTEGER NOT NULL REFERENCES differently_abled_support_types(da_support_id),
    priority INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(response_id, da_support_id)
);

CREATE INDEX idx_da_support_response ON differently_abled_support_needs(response_id);
CREATE INDEX idx_da_support_type ON differently_abled_support_needs(da_support_id);

-- =====================================================
-- SECTION 7: FARMER-SPECIFIC TABLES
-- =====================================================

-- 7.1 Farmer Details
CREATE TABLE farmer_details (
    farmer_id BIGSERIAL PRIMARY KEY,
    response_id UUID NOT NULL UNIQUE REFERENCES survey_responses(response_id) ON DELETE CASCADE,
    land_owned_acres DECIMAL(10,2),
    land_leased_acres DECIMAL(10,2),
    years_in_farming INTEGER,
    has_irrigation BOOLEAN,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_farmer_response ON farmer_details(response_id);

-- 7.2 Farmer Agriculture Interests (Many-to-Many)
CREATE TABLE farmer_agri_interests (
    fai_id BIGSERIAL PRIMARY KEY,
    response_id UUID NOT NULL REFERENCES survey_responses(response_id) ON DELETE CASCADE,
    agri_interest_id INTEGER NOT NULL REFERENCES agri_interest_types(agri_interest_id),
    is_primary BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(response_id, agri_interest_id)
);

CREATE INDEX idx_farmer_interests_response ON farmer_agri_interests(response_id);
CREATE INDEX idx_farmer_interests_type ON farmer_agri_interests(agri_interest_id);

-- 7.3 Farmer Support Needs (Many-to-Many)
CREATE TABLE farmer_support_needs (
    fsn_id BIGSERIAL PRIMARY KEY,
    response_id UUID NOT NULL REFERENCES survey_responses(response_id) ON DELETE CASCADE,
    agri_support_id INTEGER NOT NULL REFERENCES agri_support_types(agri_support_id),
    priority INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(response_id, agri_support_id)
);

CREATE INDEX idx_farmer_support_response ON farmer_support_needs(response_id);
CREATE INDEX idx_farmer_support_type ON farmer_support_needs(agri_support_id);

-- =====================================================
-- SECTION 8: LAND REQUIREMENT TABLES
-- =====================================================

-- 8.1 Land Requirements
CREATE TABLE land_requirements (
    land_req_id BIGSERIAL PRIMARY KEY,
    response_id UUID NOT NULL UNIQUE REFERENCES survey_responses(response_id) ON DELETE CASCADE,
    land_support_type_id INTEGER REFERENCES land_support_types(land_support_id),
    preferred_location TEXT,
    additional_notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_land_req_response ON land_requirements(response_id);

-- 8.2 Land Purposes Selected (Many-to-Many)
CREATE TABLE land_purposes_selected (
    lps_id BIGSERIAL PRIMARY KEY,
    response_id UUID NOT NULL REFERENCES survey_responses(response_id) ON DELETE CASCADE,
    purpose_id INTEGER NOT NULL REFERENCES land_purposes(purpose_id),
    priority INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(response_id, purpose_id)
);

CREATE INDEX idx_land_purpose_response ON land_purposes_selected(response_id);
CREATE INDEX idx_land_purpose_type ON land_purposes_selected(purpose_id);

-- =====================================================
-- SECTION 9: TIME HORIZON GOALS
-- =====================================================

CREATE TABLE time_horizon_goals (
    thg_id BIGSERIAL PRIMARY KEY,
    response_id UUID NOT NULL REFERENCES survey_responses(response_id) ON DELETE CASCADE,
    horizon_id INTEGER NOT NULL REFERENCES time_horizons(horizon_id),
    goal_type_id INTEGER NOT NULL REFERENCES goal_types(goal_type_id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(response_id, horizon_id, goal_type_id)
);

CREATE INDEX idx_th_goals_response ON time_horizon_goals(response_id);
CREATE INDEX idx_th_goals_horizon ON time_horizon_goals(horizon_id);
CREATE INDEX idx_th_goals_type ON time_horizon_goals(goal_type_id);

-- =====================================================
-- SECTION 10: SUBMISSION/ANALYTICS TABLES
-- =====================================================

-- 10.1 Submission Logs
CREATE TABLE submission_logs (
    log_id BIGSERIAL PRIMARY KEY,
    response_id UUID REFERENCES survey_responses(response_id),
    reference_id VARCHAR(20),
    submission_source VARCHAR(50),
    device_info JSONB,
    location_data JSONB,
    sync_status VARCHAR(20) DEFAULT 'completed' CHECK (sync_status IN ('pending', 'processing', 'completed', 'failed')),
    error_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_sub_log_response ON submission_logs(response_id);
CREATE INDEX idx_sub_log_status ON submission_logs(sync_status);
CREATE INDEX idx_sub_log_created ON submission_logs(created_at);

-- 10.2 Daily Aggregates (for faster dashboard queries)
CREATE TABLE daily_aggregates (
    aggregate_id BIGSERIAL PRIMARY KEY,
    aggregate_date DATE NOT NULL,
    division_id INTEGER REFERENCES revenue_divisions(division_id),
    mandal_id INTEGER REFERENCES mandals(mandal_id),
    
    -- Counts
    total_responses INTEGER DEFAULT 0,
    online_submissions INTEGER DEFAULT 0,
    offline_submissions INTEGER DEFAULT 0,
    
    -- By Age Group
    age_18_25 INTEGER DEFAULT 0,
    age_26_30 INTEGER DEFAULT 0,
    age_31_35 INTEGER DEFAULT 0,
    age_36_40 INTEGER DEFAULT 0,
    age_40_plus INTEGER DEFAULT 0,
    
    -- By Status
    homemakers INTEGER DEFAULT 0,
    students INTEGER DEFAULT 0,
    employed INTEGER DEFAULT 0,
    entrepreneurs_aspiring INTEGER DEFAULT 0,
    entrepreneurs_existing INTEGER DEFAULT 0,
    farmers INTEGER DEFAULT 0,
    differently_abled INTEGER DEFAULT 0,
    unemployed INTEGER DEFAULT 0,
    
    -- By Area Type
    rural_count INTEGER DEFAULT 0,
    urban_count INTEGER DEFAULT 0,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(aggregate_date, division_id, mandal_id)
);

CREATE INDEX idx_daily_agg_date ON daily_aggregates(aggregate_date);
CREATE INDEX idx_daily_agg_division ON daily_aggregates(division_id);
CREATE INDEX idx_daily_agg_mandal ON daily_aggregates(mandal_id);

-- =====================================================
-- SECTION 11: VIEWS FOR DASHBOARD (NALGONDA SPECIFIC)
-- =====================================================

-- 11.1 Revenue Division Distribution View
CREATE OR REPLACE VIEW vw_division_distribution AS
SELECT 
    rd.division_name,
    rd.division_code,
    COUNT(sr.response_id) as response_count,
    ROUND(COUNT(sr.response_id) * 100.0 / NULLIF(SUM(COUNT(sr.response_id)) OVER(), 0), 2) as percentage
FROM revenue_divisions rd
LEFT JOIN survey_responses sr ON rd.division_id = sr.division_id AND sr.is_complete = TRUE
GROUP BY rd.division_id, rd.division_name, rd.division_code, rd.display_order
ORDER BY rd.display_order;

-- 11.2 Mandal-wise Response Count View
CREATE OR REPLACE VIEW vw_mandal_distribution AS
SELECT 
    rd.division_name,
    m.mandal_name,
    m.mandal_code,
    COUNT(sr.response_id) as response_count
FROM mandals m
JOIN revenue_divisions rd ON m.division_id = rd.division_id
LEFT JOIN survey_responses sr ON m.mandal_id = sr.mandal_id AND sr.is_complete = TRUE
GROUP BY rd.division_name, m.mandal_id, m.mandal_name, m.mandal_code, m.display_order, rd.display_order
ORDER BY rd.display_order, m.display_order;

-- 11.3 Area Type Distribution View
CREATE OR REPLACE VIEW vw_area_type_distribution AS
SELECT 
    COALESCE(at.type_name, 'Not Specified') AS area_category,
    COUNT(*) as response_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as percentage
FROM survey_responses sr
LEFT JOIN area_types at ON sr.area_type_id = at.area_type_id
WHERE sr.is_complete = TRUE
GROUP BY at.type_name;

-- 11.4 Age Distribution View
CREATE OR REPLACE VIEW vw_age_distribution AS
SELECT 
    ag.age_range,
    COUNT(*) as response_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as percentage
FROM survey_responses sr
JOIN age_groups ag ON sr.age_group_id = ag.age_group_id
WHERE sr.is_complete = TRUE
GROUP BY ag.age_range, ag.display_order
ORDER BY ag.display_order;

-- 11.5 Women Status Distribution View
CREATE OR REPLACE VIEW vw_women_status_distribution AS
SELECT 
    ust.status_name,
    ust.status_name_telugu,
    COUNT(*) as response_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as percentage
FROM survey_responses sr
JOIN user_status_types ust ON sr.user_status_id = ust.status_id
WHERE sr.is_complete = TRUE
GROUP BY ust.status_name, ust.status_name_telugu, ust.display_order
ORDER BY ust.display_order;

-- 11.6 Top Interests View
CREATE OR REPLACE VIEW vw_top_interests AS
SELECT 
    it.interest_name,
    it.interest_name_telugu,
    COUNT(*) as interest_count
FROM survey_interests si
JOIN interest_types it ON si.interest_id = it.interest_id
JOIN survey_responses sr ON si.response_id = sr.response_id
WHERE sr.is_complete = TRUE
GROUP BY it.interest_name, it.interest_name_telugu, it.display_order
ORDER BY interest_count DESC;

-- 11.7 Support Demand View
CREATE OR REPLACE VIEW vw_support_demand AS
SELECT 
    st.support_name,
    st.support_name_telugu,
    COUNT(*) as demand_count
FROM survey_support_needs ssn
JOIN support_types st ON ssn.support_id = st.support_id
JOIN survey_responses sr ON ssn.response_id = sr.response_id
WHERE sr.is_complete = TRUE
GROUP BY st.support_name, st.support_name_telugu, st.display_order
ORDER BY demand_count DESC;

-- 11.8 Entrepreneur Funnel View
CREATE OR REPLACE VIEW vw_entrepreneur_funnel AS
SELECT 
    entrepreneur_stage as stage,
    COUNT(*) as count
FROM survey_responses
WHERE is_complete = TRUE AND entrepreneur_stage IS NOT NULL
GROUP BY entrepreneur_stage
ORDER BY 
    CASE entrepreneur_stage 
        WHEN 'ASPIRING' THEN 1 
        WHEN 'EXISTING' THEN 2 
        WHEN 'GROWTH' THEN 3 
    END;

-- 11.9 Mandal Priority Index View (based on response count)
CREATE OR REPLACE VIEW vw_mandal_priority AS
SELECT 
    m.mandal_name,
    m.mandal_code,
    rd.division_name,
    COUNT(sr.response_id) as response_count,
    RANK() OVER (ORDER BY COUNT(sr.response_id) DESC) as priority_rank
FROM mandals m
JOIN revenue_divisions rd ON m.division_id = rd.division_id
LEFT JOIN survey_responses sr ON m.mandal_id = sr.mandal_id AND sr.is_complete = TRUE
GROUP BY m.mandal_id, m.mandal_name, m.mandal_code, rd.division_name
ORDER BY response_count DESC
LIMIT 10;

-- 11.10 Submission Mode Distribution View
CREATE OR REPLACE VIEW vw_submission_mode AS
SELECT 
    submission_mode,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as percentage
FROM survey_responses
WHERE is_complete = TRUE
GROUP BY submission_mode;

-- 11.11 Differently-Abled Needs View
CREATE OR REPLACE VIEW vw_differently_abled_needs AS
SELECT 
    dst.support_name,
    dst.support_name_telugu,
    COUNT(*) as need_count
FROM differently_abled_support_needs dasn
JOIN differently_abled_support_types dst ON dasn.da_support_id = dst.da_support_id
JOIN survey_responses sr ON dasn.response_id = sr.response_id
WHERE sr.is_complete = TRUE
GROUP BY dst.support_name, dst.support_name_telugu, dst.display_order
ORDER BY need_count DESC;

-- 11.12 Agri Interests View
CREATE OR REPLACE VIEW vw_agri_interests AS
SELECT 
    ait.interest_name,
    ait.interest_name_telugu,
    COUNT(*) as interest_count
FROM farmer_agri_interests fai
JOIN agri_interest_types ait ON fai.agri_interest_id = ait.agri_interest_id
JOIN survey_responses sr ON fai.response_id = sr.response_id
WHERE sr.is_complete = TRUE
GROUP BY ait.interest_name, ait.interest_name_telugu, ait.display_order
ORDER BY interest_count DESC;

-- 11.13 Dashboard Summary View (Nalgonda Specific)
CREATE OR REPLACE VIEW vw_dashboard_summary AS
SELECT 
    d.district_name,
    d.state_name,
    COUNT(sr.response_id) as total_responses,
    COUNT(DISTINCT sr.division_id) as divisions_covered,
    COUNT(DISTINCT sr.mandal_id) as mandals_covered,
    SUM(CASE WHEN submission_mode = 'ONLINE' THEN 1 ELSE 0 END) as online_submissions,
    SUM(CASE WHEN submission_mode = 'OFFLINE' THEN 1 ELSE 0 END) as offline_submissions,
    MIN(sr.created_at) as first_response,
    MAX(sr.created_at) as last_response
FROM districts d
LEFT JOIN survey_responses sr ON d.district_id = sr.district_id AND sr.is_complete = TRUE
WHERE d.district_code = 'NLG'
GROUP BY d.district_id, d.district_name, d.state_name;

-- 11.14 Village-wise Response Summary
CREATE OR REPLACE VIEW vw_village_summary AS
SELECT 
    rd.division_name,
    m.mandal_name,
    sr.village_area_name,
    COUNT(*) as response_count
FROM survey_responses sr
JOIN revenue_divisions rd ON sr.division_id = rd.division_id
JOIN mandals m ON sr.mandal_id = m.mandal_id
WHERE sr.is_complete = TRUE
GROUP BY rd.division_name, m.mandal_name, sr.village_area_name
ORDER BY rd.division_name, m.mandal_name, response_count DESC;

-- =====================================================
-- SECTION 12: FUNCTIONS AND TRIGGERS
-- =====================================================

-- 12.1 Function to generate reference ID (Nalgonda specific)
CREATE OR REPLACE FUNCTION generate_reference_id() 
RETURNS VARCHAR(20) AS $$
DECLARE
    chars VARCHAR := 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
    result VARCHAR := 'WE-NLG-';
    i INTEGER;
BEGIN
    FOR i IN 1..6 LOOP
        result := result || substr(chars, floor(random() * length(chars) + 1)::INTEGER, 1);
    END LOOP;
    RETURN result;
END;
$$ LANGUAGE plpgsql;

-- 12.2 Trigger to auto-generate reference ID
CREATE OR REPLACE FUNCTION set_reference_id()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.reference_id IS NULL THEN
        LOOP
            NEW.reference_id := generate_reference_id();
            EXIT WHEN NOT EXISTS (SELECT 1 FROM survey_responses WHERE reference_id = NEW.reference_id);
        END LOOP;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_set_reference_id
    BEFORE INSERT ON survey_responses
    FOR EACH ROW
    EXECUTE FUNCTION set_reference_id();

-- 12.3 Function to update timestamps
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply update timestamp triggers
CREATE TRIGGER trg_districts_updated_at BEFORE UPDATE ON districts FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER trg_revenue_divisions_updated_at BEFORE UPDATE ON revenue_divisions FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER trg_mandals_updated_at BEFORE UPDATE ON mandals FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER trg_admin_users_updated_at BEFORE UPDATE ON admin_users FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER trg_survey_responses_updated_at BEFORE UPDATE ON survey_responses FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER trg_entrepreneur_details_updated_at BEFORE UPDATE ON entrepreneur_details FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER trg_differently_abled_details_updated_at BEFORE UPDATE ON differently_abled_details FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER trg_farmer_details_updated_at BEFORE UPDATE ON farmer_details FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER trg_land_requirements_updated_at BEFORE UPDATE ON land_requirements FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER trg_daily_aggregates_updated_at BEFORE UPDATE ON daily_aggregates FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- 12.4 Function to validate mandal belongs to selected division
CREATE OR REPLACE FUNCTION validate_mandal_division()
RETURNS TRIGGER AS $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM mandals 
        WHERE mandal_id = NEW.mandal_id 
        AND division_id = NEW.division_id
    ) THEN
        RAISE EXCEPTION 'Mandal % does not belong to Division %', NEW.mandal_id, NEW.division_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_validate_mandal_division
    BEFORE INSERT OR UPDATE ON survey_responses
    FOR EACH ROW
    EXECUTE FUNCTION validate_mandal_division();

-- 12.5 Function to refresh daily aggregates
CREATE OR REPLACE FUNCTION refresh_daily_aggregates(p_date DATE DEFAULT CURRENT_DATE)
RETURNS VOID AS $$
BEGIN
    INSERT INTO daily_aggregates (
        aggregate_date, division_id, mandal_id, total_responses, online_submissions, offline_submissions,
        age_18_25, age_26_30, age_31_35, age_36_40, age_40_plus,
        homemakers, students, employed, entrepreneurs_aspiring, entrepreneurs_existing,
        farmers, differently_abled, unemployed, rural_count, urban_count
    )
    SELECT 
        p_date,
        sr.division_id,
        sr.mandal_id,
        COUNT(*),
        SUM(CASE WHEN submission_mode = 'ONLINE' THEN 1 ELSE 0 END),
        SUM(CASE WHEN submission_mode = 'OFFLINE' THEN 1 ELSE 0 END),
        SUM(CASE WHEN ag.age_range = '18-25' THEN 1 ELSE 0 END),
        SUM(CASE WHEN ag.age_range = '26-30' THEN 1 ELSE 0 END),
        SUM(CASE WHEN ag.age_range = '31-35' THEN 1 ELSE 0 END),
        SUM(CASE WHEN ag.age_range = '36-40' THEN 1 ELSE 0 END),
        SUM(CASE WHEN ag.age_range = '40+' THEN 1 ELSE 0 END),
        SUM(CASE WHEN ust.status_code = 'HOMEMAKER' THEN 1 ELSE 0 END),
        SUM(CASE WHEN ust.status_code = 'STUDENT' THEN 1 ELSE 0 END),
        SUM(CASE WHEN ust.status_code = 'EMPLOYED' THEN 1 ELSE 0 END),
        SUM(CASE WHEN ust.status_code = 'ENTREPRENEUR_ASPIRING' THEN 1 ELSE 0 END),
        SUM(CASE WHEN ust.status_code = 'ENTREPRENEUR_EXISTING' THEN 1 ELSE 0 END),
        SUM(CASE WHEN ust.status_code = 'FARMER' THEN 1 ELSE 0 END),
        SUM(CASE WHEN ust.status_code = 'DIFFERENTLY_ABLED' THEN 1 ELSE 0 END),
        SUM(CASE WHEN ust.status_code = 'UNEMPLOYED' THEN 1 ELSE 0 END),
        SUM(CASE WHEN at.type_code = 'RURAL' THEN 1 ELSE 0 END),
        SUM(CASE WHEN at.type_code IN ('URBAN', 'SEMI_URBAN') THEN 1 ELSE 0 END)
    FROM survey_responses sr
    JOIN age_groups ag ON sr.age_group_id = ag.age_group_id
    JOIN user_status_types ust ON sr.user_status_id = ust.status_id
    LEFT JOIN area_types at ON sr.area_type_id = at.area_type_id
    WHERE sr.is_complete = TRUE AND DATE(sr.created_at) = p_date
    GROUP BY sr.division_id, sr.mandal_id
    ON CONFLICT (aggregate_date, division_id, mandal_id) DO UPDATE SET
        total_responses = EXCLUDED.total_responses,
        online_submissions = EXCLUDED.online_submissions,
        offline_submissions = EXCLUDED.offline_submissions,
        age_18_25 = EXCLUDED.age_18_25,
        age_26_30 = EXCLUDED.age_26_30,
        age_31_35 = EXCLUDED.age_31_35,
        age_36_40 = EXCLUDED.age_36_40,
        age_40_plus = EXCLUDED.age_40_plus,
        homemakers = EXCLUDED.homemakers,
        students = EXCLUDED.students,
        employed = EXCLUDED.employed,
        entrepreneurs_aspiring = EXCLUDED.entrepreneurs_aspiring,
        entrepreneurs_existing = EXCLUDED.entrepreneurs_existing,
        farmers = EXCLUDED.farmers,
        differently_abled = EXCLUDED.differently_abled,
        unemployed = EXCLUDED.unemployed,
        rural_count = EXCLUDED.rural_count,
        urban_count = EXCLUDED.urban_count,
        updated_at = CURRENT_TIMESTAMP;
END;
$$ LANGUAGE plpgsql;

-- =====================================================
-- SECTION 13: API HELPER FUNCTIONS
-- =====================================================

-- 13.1 Get Mandals by Division (for cascading dropdown)
CREATE OR REPLACE FUNCTION get_mandals_by_division(p_division_id INTEGER)
RETURNS TABLE (
    mandal_id INTEGER,
    mandal_code VARCHAR(20),
    mandal_name VARCHAR(150),
    local_name VARCHAR(150)
) AS $$
BEGIN
    RETURN QUERY
    SELECT m.mandal_id, m.mandal_code, m.mandal_name, m.local_name
    FROM mandals m
    WHERE m.division_id = p_division_id AND m.is_active = TRUE
    ORDER BY m.display_order;
END;
$$ LANGUAGE plpgsql;

-- 13.2 Get All Revenue Divisions (for dropdown)
CREATE OR REPLACE FUNCTION get_revenue_divisions()
RETURNS TABLE (
    division_id INTEGER,
    division_code VARCHAR(20),
    division_name VARCHAR(100),
    total_mandals INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT rd.division_id, rd.division_code, rd.division_name, rd.total_mandals
    FROM revenue_divisions rd
    WHERE rd.is_active = TRUE
    ORDER BY rd.display_order;
END;
$$ LANGUAGE plpgsql;

-- =====================================================
-- END OF DATABASE SCHEMA - NALGONDA DISTRICT
-- =====================================================
