// Mock data for initial prototyping
// Realistic synthetic data for villa rental knowledge assistant domain

export interface User {
  id: string;
  email: string;
  name: string;
  role: 'agent' | 'expert' | 'admin';
  created_at: string;
  updated_at: string;
}

export interface Villa {
  id: string;
  name: string;
  location: string;
  country: string;
  description: string;
  bedrooms: number;
  max_guests: number;
  price_per_night: number;
  amenities: string[];
  images: string[];
  created_at: string;
}

export interface KnowledgeSource {
  id: string;
  title: string;
  type: 'faq' | 'review' | 'crm' | 'policy' | 'manual';
  content: string;
  source_url?: string;
  uploaded_by: string;
  uploaded_at: string;
  tags: string[];
}

export interface Answer {
  id: string;
  question: string;
  answer: string;
  confidence: number;
  created_by: string;
  created_at: string;
  updated_at: string;
  status: 'approved' | 'pending_review' | 'corrected';
  metadata?: Record<string, any>;
}

export interface Citation {
  id: string;
  answer_id: string;
  source_id: string;
  excerpt: string;
  relevance_score: number;
  start_position: number;
  end_position: number;
  highlighted_text?: string;
}

export interface ExpertCorrection {
  id: string;
  answer_id: string;
  submitted_by: string;
  corrected_answer: string;
  reason: 'inaccurate' | 'incomplete' | 'outdated' | 'ambiguous';
  status: 'pending' | 'approved' | 'rejected';
  submitted_at: string;
  reviewed_at?: string;
  reviewed_by?: string;
  notes?: string;
}

export interface CoverageGap {
  id: string;
  topic: string;
  category: string;
  gap_description: string;
  priority: 'high' | 'medium' | 'low';
  detected_at: string;
  resolved_at?: string;
  assigned_to?: string;
}

export interface AuditLog {
  id: string;
  user_id: string;
  action: string;
  entity_type: string;
  entity_id: string;
  details: Record<string, any>;
  ip_address?: string;
  user_agent?: string;
  created_at: string;
}

// Mock data instances
export const mockData = {
  users: [
    {
      id: 'user-001',
      email: 'john.agent@cv-villas.com',
      name: 'John Smith',
      role: 'agent',
      created_at: '2024-01-15T10:30:00Z',
      updated_at: '2024-01-15T10:30:00Z',
    },
    {
      id: 'user-002',
      email: 'sarah.expert@cv-villas.com',
      name: 'Dr. Sarah Chen',
      role: 'expert',
      created_at: '2024-01-16T14:20:00Z',
      updated_at: '2024-01-16T14:20:00Z',
    },
    {
      id: 'user-003',
      email: 'mike.admin@cv-villas.com',
      name: 'Mike Rodriguez',
      role: 'admin',
      created_at: '2024-01-10T09:15:00Z',
      updated_at: '2024-01-10T09:15:00Z',
    },
    {
      id: 'user-004',
      email: 'lisa.agent@cv-villas.fr',
      name: 'Lisa Dubois',
      role: 'agent',
      created_at: '2024-02-01T11:45:00Z',
      updated_at: '2024-02-01T11:45:00Z',
    },
    {
      id: 'user-005',
      email: 'alex.expert@cv-villas.es',
      name: 'Alex García',
      role: 'expert',
      created_at: '2024-01-20T16:30:00Z',
      updated_at: '2024-01-20T16:30:00Z',
    },
    {
      id: 'user-006',
      email: 'maria.agent@cv-villas.it',
      name: 'Maria Rossi',
      role: 'agent',
      created_at: '2024-02-05T08:20:00Z',
      updated_at: '2024-02-05T08:20:00Z',
    },
    {
      id: 'user-007',
      email: 'thomas.agent@cv-villas.de',
      name: 'Thomas Schmidt',
      role: 'agent',
      created_at: '2024-01-25T13:10:00Z',
      updated_at: '2024-01-25T13:10:00Z',
    },
    {
      id: 'user-008',
      email: 'emma.admin@cv-villas.com',
      name: 'Emma Wilson',
      role: 'admin',
      created_at: '2024-01-18T15:40:00Z',
      updated_at: '2024-01-18T15:40:00Z',
    },
  ] as User[],

  villas: [
    {
      id: 'villa-001',
      name: 'Villa Serenity',
      location: 'Santorini, Greece',
      country: 'Greece',
      description: 'A stunning cliffside villa with panoramic views of the Aegean Sea. Features infinity pool, outdoor dining area, and private access to a secluded beach.',
      bedrooms: 4,
      max_guests: 8,
      price_per_night: 1200,
      amenities: ['Infinity Pool', 'Private Beach', 'Wine Cellar', 'Outdoor Kitchen', 'Hot Tub', 'Concierge'],
      images: ['villa-serinity-1.jpg', 'villa-serinity-2.jpg'],
      created_at: '2023-12-01T10:00:00Z',
    },
    {
      id: 'villa-002',
      name: 'Casa del Sol',
      location: 'Tuscany, Italy',
      country: 'Italy',
      description: 'A rustic Tuscan villa surrounded by vineyards and olive groves. Features historic architecture, wine tasting room, and chef\'s kitchen.',
      bedrooms: 6,
      max_guests: 12,
      price_per_night: 1500,
      amenities: ['Vineyard Views', 'Wine Tasting Room', 'Fireplace', 'Gardens', 'Pet Friendly', 'Chef Available'],
      images: ['casa-del-sol-1.jpg', 'casa-del-sol-2.jpg'],
      created_at: '2023-11-15T14:30:00Z',
    },
    {
      id: 'villa-003',
      name: 'Villa Azure',
      location: 'Bali, Indonesia',
      country: 'Indonesia',
      description: 'Luxury beachfront villa with traditional Balinese architecture. Features private temple, spa services, and direct beach access.',
      bedrooms: 5,
      max_guests: 10,
      price_per_night: 900,
      amenities: ['Private Beach', 'Spa', 'Yoga Pavilion', 'Chef Services', 'Meditation Garden', 'Butler'],
      images: ['villa-azure-1.jpg', 'villa-azure-2.jpg'],
      created_at: '2024-01-10T09:45:00Z',
    },
    {
      id: 'villa-004',
      name: 'Château Blanc',
      location: 'Provence, France',
      country: 'France',
      description: '18th-century French château with formal gardens and lavender fields. Features antique furniture, grand ballroom, and wine cellar.',
      bedrooms: 8,
      max_guests: 16,
      price_per_night: 2500,
      amenities: ['Formal Gardens', 'Ballroom', 'Library', 'Wine Cellar', 'Helipad', 'Staff of 8'],
      images: ['chateau-blanc-1.jpg', 'chateau-blanc-2.jpg'],
      created_at: '2023-10-20T16:20:00Z',
    },
    {
      id: 'villa-005',
      name: 'Ocean View Retreat',
      location: 'Big Sur, California',
      country: 'USA',
      description: 'Modern architectural masterpiece perched on cliffs overlooking the Pacific Ocean. Features floor-to-ceiling windows, indoor waterfall, and observatory.',
      bedrooms: 3,
      max_guests: 6,
      price_per_night: 1800,
      amenities: ['Ocean Views', 'Observatory', 'Home Theater', 'Smart Home', 'Electric Car Charger', 'Private Trail'],
      images: ['ocean-view-retreat-1.jpg', 'ocean-view-retreat-2.jpg'],
      created_at: '2024-02-01T11:15:00Z',
    },
    {
      id: 'villa-006',
      name: 'Mountain Haven',
      location: 'Aspen, Colorado',
      country: 'USA',
      description: 'Ski-in/ski-out luxury chalet with stunning mountain views. Features private ski lift, hot tub, and apres-ski lounge.',
      bedrooms: 5,
      max_guests: 10,
      price_per_night: 1600,
      amenities: ['Ski-in/Ski-out', 'Hot Tub', 'Fireplace', 'Game Room', 'Wine Cave', 'Garage'],
      images: ['mountain-haven-1.jpg', 'mountain-haven-2.jpg'],
      created_at: '2023-12-15T13:40:00Z',
    },
    {
      id: 'villa-007',
      name: 'Tropical Oasis',
      location: 'Phuket, Thailand',
      country: 'Thailand',
      description: 'Contemporary villa nestled in tropical gardens with multiple pools and pavilions. Features traditional Thai massage sala and private chef.',
      bedrooms: 4,
      max_guests: 8,
      price_per_night: 750,
      amenities: ['Multiple Pools', 'Massage Sala', 'Private Chef', 'Tropical Gardens', 'Beach Access', 'Kayaks'],
      images: ['tropical-oasis-1.jpg', 'tropical-oasis-2.jpg'],
      created_at: '2024-01-05T15:20:00Z',
    },
    {
      id: 'villa-008',
      name: 'Desert Mirage',
      location: 'Dubai, UAE',
      country: 'UAE',
      description: 'Ultra-modern villa in exclusive Dubai community with gold fixtures and cutting-edge technology. Features private cinema and indoor pool.',
      bedrooms: 7,
      max_guests: 14,
      price_per_night: 3000,
      amenities: ['Indoor Pool', 'Private Cinema', 'Smart Home', 'Gold Fixtures', 'Helipad', '24/7 Concierge'],
      images: ['desert-mirage-1.jpg', 'desert-mirage-2.jpg'],
      created_at: '2023-11-30T10:50:00Z',
    },
    {
      id: 'villa-009',
      name: 'Historic Manor',
      location: 'Cornwall, England',
      country: 'UK',
      description: 'Grade II listed historic manor house with period features and extensive grounds. Features working fireplaces and antique furnishings.',
      bedrooms: 6,
      max_guests: 12,
      price_per_night: 1400,
      amenities: ['Historic Features', 'Formal Gardens', 'Library', 'Tennis Court', 'Greenhouse', 'Caretaker'],
      images: ['historic-manor-1.jpg', 'historic-manor-2.jpg'],
      created_at: '2023-12-20T12:30:00Z',
    },
    {
      id: 'villa-010',
      name: 'Island Escape',
      location: 'Maldives',
      country: 'Maldives',
      description: 'Overwater villa with glass floor panels and direct lagoon access. Features private infinity pool and outdoor shower.',
      bedrooms: 2,
      max_guests: 4,
      price_per_night: 1100,
      amenities: ['Overwater Villa', 'Glass Floor', 'Infinity Pool', 'Snorkeling Gear', 'Private Chef', 'Spa Treatments'],
      images: ['island-escape-1.jpg', 'island-escape-2.jpg'],
      created_at: '2024-01-25T14:15:00Z',
    },
  ] as Villa[],

  knowledgeSources: [
    {
      id: 'source-001',
      title: 'FAQ-2024-Villa-Santorini',
      type: 'faq',
      content: 'Q: What is the cancellation policy for Villa Serenity?\nA: Cancellations made 60+ days before arrival receive full refund. 30-60 days: 50% refund. Less than 30 days: no refund.\n\nQ: Is airport transfer included?\nA: Yes, complimentary airport transfer is provided for stays of 7+ nights.\n\nQ: Are pets allowed?\nA: No pets allowed due to villa design and local regulations.',
      source_url: 'https://internal.cv-villas.com/faq/santorini',
      uploaded_by: 'user-002',
      uploaded_at: '2024-01-20T11:30:00Z',
      tags: ['santorini', 'cancellation', 'pets', 'airport'],
    },
    {
      id: 'source-002',
      title: 'Customer Review - Villa Azure',
      type: 'review',
      content: 'The villa exceeded all expectations. The private beach was pristine, and the staff was exceptional. The spa treatments were world-class. Highly recommend the sunset yoga sessions.',
      source_url: 'https://reviews.cv-villas.com/bali/villa-azure',
      uploaded_by: 'user-001',
      uploaded_at: '2024-02-05T14:25:00Z',
      tags: ['bali', 'reviews', 'spa', 'staff'],
    },
    {
      id: 'source-003',
      title: 'CRM Notes - Casa del Sol',
      type: 'crm',
      content: 'Client #4321 prefers prosecco over champagne. Special dietary requirements: gluten-free. Anniversary celebration on 2024-06-15 - arrange flowers and cake.',
      source_url: 'https://crm.cv-villas.com/clients/4321',
      uploaded_by: 'user-004',
      uploaded_at: '2024-01-30T10:15:00Z',
      tags: ['tuscany', 'client-preferences', 'dietary', 'celebrations'],
    },
    {
      id: 'source-004',
      title: 'Cleaning Policy Handbook',
      type: 'policy',
      content: 'All villas undergo deep cleaning between guests. Special COVID-19 protocol includes UV sanitization of high-touch surfaces. Guests must vacate property by 10AM for cleaning team access.',
      source_url: 'https://docs.cv-villas.com/policies/cleaning',
      uploaded_by: 'user-003',
      uploaded_at: '2024-01-12T09:45:00Z',
      tags: ['cleaning', 'safety', 'covid', 'checkout'],
    },
    {
      id: 'source-005',
      title: 'Wine Collection Manual',
      type: 'manual',
      content: 'Casa del Sol wine cellar inventory includes 200+ bottles. Important: Serve Chianti Classico 2018 at 18°C. Restock weekly. Expert guests may request private tastings.',
      source_url: 'https://manuals.cv-villas.com/wine-collection',
      uploaded_by: 'user-005',
      uploaded_at: '2024-01-25T16:40:00Z',
      tags: ['wine', 'tuscany', 'cellar', 'inventory'],
    },
    {
      id: 'source-006',
      title: 'Seasonal Pricing Guide 2024',
      type: 'policy',
      content: 'High season: June-August + December 20-January 5: 20% premium. Shoulder season: April-May + September-October: standard rates. Low season: November-March (excluding Christmas): 15% discount.',
      source_url: 'https://docs.cv-villas.com/pricing/2024',
      uploaded_by: 'user-008',
      uploaded_at: '2023-12-15T14:20:00Z',
      tags: ['pricing', 'seasonal', '2024', 'rates'],
    },
    {
      id: 'source-007',
      title: 'Sustainability Guidelines',
      type: 'policy',
      content: 'All villas implement water conservation measures. Organic local produce prioritized. Solar panels mandatory for new builds. Waste recycling programs in place.',
      source_url: 'https://docs.cv-villas.com/sustainability',
      uploaded_by: 'user-002',
      uploaded_at: '2024-02-01T11:10:00Z',
      tags: ['sustainability', 'environment', 'recycling', 'solar'],
    },
    {
      id: 'source-008',
      title: 'Emergency Procedures',
      type: 'manual',
      content: 'Emergency contact: +1-800-VILLA-911. Medical facilities mapped for each location. Natural disaster evacuation plans available. Staff trained in basic first aid.',
      source_url: 'https://manuals.cv-villas.com/emergency',
      uploaded_by: 'user-003',
      uploaded_at: '2024-01-18T13:55:00Z',
      tags: ['emergency', 'safety', 'medical', 'contacts'],
    },
    {
      id: 'source-009',
      title: 'Guest Experience Standards',
      type: 'manual',
      content: 'Welcome basket must include local specialties. Check-in within 15 minutes of guest arrival. 24/7 concierge response time: under 10 minutes. Guest feedback follow-up within 48 hours.',
      source_url: 'https://manuals.cv-villas.com/guest-experience',
      uploaded_by: 'user-007',
      uploaded_at: '2024-01-22T15:30:00Z',
      tags: ['guest-experience', 'concierge', 'standards', 'service'],
    },
    {
      id: 'source-010',
      title: 'Maintenance Schedule',
      type: 'manual',
      content: 'Pool maintenance: weekly chemical checks. HVAC filter replacement: quarterly. Security system testing: monthly. Appliance servicing: bi-annually.',
      source_url: 'https://manuals.cv-villas.com/maintenance',
      uploaded_by: 'user-006',
      uploaded_at: '2024-01-28T09:20:00Z',
      tags: ['maintenance', 'pool', 'hvac', 'security'],
    },
    // Additional sources to reach 20 total
    ...Array.from({ length: 10 }, (_, i) => ({
      id: `source-${String(i + 11).padStart(3, '0')}`,
      title: `Villa Documentation ${i + 11}`,
      type: ['faq', 'review', 'crm', 'policy', 'manual'][i % 5] as any,
      content: `Sample content for source ${i + 11} covering various villa topics and operational details.`,
      uploaded_by: `user-${String((i % 8) + 1).padStart(3, '0')}`,
      uploaded_at: `2024-01-${String(15 + i).padStart(2, '0')}T${String(10 + i).padStart(2, '0')}:30:00Z`,
      tags: [`topic${i + 1}`, 'documentation', 'reference'],
    })),
  ] as KnowledgeSource[],

  answers: [
    {
      id: 'answer-001',
      question: 'What is the cancellation policy?',
      answer: 'Cancellation policies vary by villa and season. Generally, full refund if cancelled 60+ days before arrival. 50% refund for 30-60 days. No refund within 30 days. Check specific villa FAQ for details.',
      confidence: 0.95,
      created_by: 'user-002',
      created_at: '2024-02-10T14:30:00Z',
      updated_at: '2024-02-10T14:30:00Z',
      status: 'approved',
      metadata: { villa_ids: ['villa-001', 'villa-002'] },
    },
    {
      id: 'answer-002',
      question: 'Are pets allowed at Villa Serenity?',
      answer: 'No, pets are not allowed at Villa Serenity due to the villa design and local regulations.',
      confidence: 0.98,
      created_by: 'user-001',
      created_at: '2024-02-11T09:15:00Z',
      updated_at: '2024-02-11T09:15:00Z',
      status: 'approved',
      metadata: { villa_ids: ['villa-001'] },
    },
    {
      id: 'answer-003',
      question: 'What amenities are included?',
      answer: 'Standard amenities include WiFi, air conditioning, and basic kitchen equipment. Premium amenities vary by villa and may include pools, hot tubs, private chefs, concierge services, and recreational equipment.',
      confidence: 0.87,
      created_by: 'user-005',
      created_at: '2024-02-09T16:45:00Z',
      updated_at: '2024-02-09T16:45:00Z',
      status: 'approved',
      metadata: { villa_ids: ['villa-003', 'villa-004'] },
    },
    {
      id: 'answer-004',
      question: 'How does airport transfer work?',
      answer: 'Complimentary airport transfer is provided for stays of 7 nights or longer at most villas. For shorter stays, transfers can be arranged for an additional fee.',
      confidence: 0.92,
      created_by: 'user-002',
      created_at: '2024-02-08T11:20:00Z',
      updated_at: '2024-02-08T11:20:00Z',
      status: 'approved',
      metadata: { villa_ids: ['villa-001', 'villa-005'] },
    },
    {
      id: 'answer-005',
      question: 'What is the check-in/check-out time?',
      answer: 'Standard check-in is 3:00 PM and check-out is 11:00 AM. Early check-in or late check-out may be available upon request, subject to availability.',
      confidence: 0.96,
      created_by: 'user-001',
      created_at: '2024-02-07T10:05:00Z',
      updated_at: '2024-02-07T10:05:00Z',
      status: 'approved',
      metadata: { villa_ids: [] },
    },
    // Additional answers
    ...Array.from({ length: 10 }, (_, i) => ({
      id: `answer-${String(i + 6).padStart(3, '0')}`,
      question: `Sample question about villa ${i + 1}`,
      answer: `This is a sample answer providing information on villa topic ${i + 1}.`,
      confidence: 0.7 + (i * 0.03),
      created_by: `user-${String((i % 8) + 1).padStart(3, '0')}`,
      created_at: `2024-02-${String(5 + i).padStart(2, '0')}T${String(9 + i).padStart(2, '0')}:${String(15 + (i * 5) % 60).padStart(2, '0')}:00Z`,
      updated_at: `2024-02-${String(5 + i).padStart(2, '0')}T${String(9 + i).padStart(2, '0')}:${String(15 + (i * 5) % 60).padStart(2, '0')}:00Z`,
      status: ['approved', 'pending_review', 'corrected'][i % 3] as any,
      metadata: { villa_ids: [`villa-${String((i % 10) + 1).padStart(3, '0')}`] },
    })),
  ] as Answer[],

  citations: Array.from({ length: 30 }, (_, i) => ({
    id: `citation-${String(i + 1).padStart(3, '0')}`,
    answer_id: `answer-${String((i % 15) + 1).padStart(3, '0')}`,
    source_id: `source-${String((i % 20) + 1).padStart(3, '0')}`,
    excerpt: `This is an excerpt from source ${(i % 20) + 1} supporting answer ${(i % 15) + 1}.`,
    relevance_score: 0.5 + (i * 0.015),
    start_position: i * 100,
    end_position: i * 100 + 50,
    highlighted_text: i % 5 === 0 ? `highlighted text ${i}` : undefined,
  })) as Citation[],

  expertCorrections: [
    {
      id: 'correction-001',
      answer_id: 'answer-003',
      submitted_by: 'user-005',
      corrected_answer: 'Standard amenities include WiFi, air conditioning, basic kitchen equipment, and linens. Premium amenities vary by villa and may include pools, hot tubs, private chefs, concierge services, recreational equipment, and daily housekeeping.',
      reason: 'incomplete',
      status: 'approved',
      submitted_at: '2024-02-12T14:30:00Z',
      reviewed_at: '2024-02-13T10:15:00Z',
      reviewed_by: 'user-002',
      notes: 'Added linens and daily housekeeping to standard amenities.',
    },
    {
      id: 'correction-002',
      answer_id: 'answer-001',
      submitted_by: 'user-002',
      corrected_answer: 'Cancellation policies vary by villa and season. Generally, full refund if cancelled 60+ days before arrival. 50% refund for 30-60 days. No refund within 30 days. Some premium villas have stricter policies - always check specific villa FAQ.',
      reason: 'inaccurate',
      status: 'pending',
      submitted_at: '2024-02-14T11:20:00Z',
      notes: 'Added note about premium villas having stricter policies.',
    },
    // Additional corrections
    ...Array.from({ length: 8 }, (_, i) => ({
      id: `correction-${String(i + 3).padStart(3, '0')}`,
      answer_id: `answer-${String((i % 15) + 1).padStart(3, '0')}`,
      submitted_by: `user-${String((i % 8) + 1).padStart(3, '0')}`,
      corrected_answer: `Corrected answer version ${i + 1} with improved accuracy.`,
      reason: ['inaccurate', 'incomplete', 'outdated', 'ambiguous'][i % 4] as any,
      status: ['pending', 'approved', 'rejected'][i % 3] as any,
      submitted_at: `2024-02-${String(10 + i).padStart(2, '0')}T${String(9 + i).padStart(2, '0')}:00:00Z`,
      reviewed_at: i % 2 === 0 ? `2024-02-${String(11 + i).padStart(2, '0')}T${String(10 + i).padStart(2, '0')}:00:00Z` : undefined,
      reviewed_by: i % 2 === 0 ? `user-${String(((i + 1) % 8) + 1).padStart(3, '0')}` : undefined,
      notes: i % 3 === 0 ? `Correction note ${i + 1}` : undefined,
    })),
  ] as ExpertCorrection[],

  coverageGaps: [
    {
      id: 'gap-001',
      topic: 'Sustainable Practices',
      category: 'Environmental',
      gap_description: 'Limited information on villa-specific sustainability initiatives and local environmental impact.',
      priority: 'high',
      detected_at: '2024-02-01T09:15:00Z',
      assigned_to: 'user-002',
    },
    {
      id: 'gap-002',
      topic: 'Accessibility Features',
      category: 'Guest Experience',
      gap_description: 'Incomplete data on wheelchair accessibility, hearing/visual impairment accommodations.',
      priority: 'medium',
      detected_at: '2024-02-03T14:30:00Z',
      resolved_at: '2024-02-10T11:45:00Z',
      assigned_to: 'user-004',
    },
    {
      id: 'gap-003',
      topic: 'Local Dining Recommendations',
      category: 'Concierge',
      gap_description: 'Limited restaurant recommendations beyond major tourist areas.',
      priority: 'low',
      detected_at: '2024-02-05T16:20:00Z',
      assigned_to: 'user-001',
    },
    // Additional coverage gaps
    ...Array.from({ length: 7 }, (_, i) => ({
      id: `gap-${String(i + 4).padStart(3, '0')}`,
      topic: `Topic ${i + 4}`,
      category: ['Environmental', 'Guest Experience', 'Concierge', 'Maintenance', 'Pricing'][i % 5],
      gap_description: `Gap description for topic ${i + 4} requiring additional knowledge source coverage.`,
      priority: ['high', 'medium', 'low'][i % 3] as any,
      detected_at: `2024-02-${String(6 + i).padStart(2, '0')}T${String(10 + i).padStart(2, '0')}:00:00Z`,
      resolved_at: i % 4 === 0 ? `2024-02-${String(13 + i).padStart(2, '0')}T${String(11 + i).padStart(2, '0')}:00:00Z` : undefined,
      assigned_to: i % 3 === 0 ? `user-${String(((i + 2) % 8) + 1).padStart(3, '0')}` : undefined,
    })),
  ] as CoverageGap[],

  auditLogs: Array.from({ length: 25 }, (_, i) => ({
    id: `audit-${String(i + 1).padStart(3, '0')}`,
    user_id: `user-${String((i % 8) + 1).padStart(3, '0')}`,
    action: ['LOGIN', 'LOGOUT', 'VIEW_ANSWER', 'SUBMIT_QUESTION', 'CORRECTION_SUBMITTED', 'ADMIN_ACTION'][i % 6],
    entity_type: i % 3 === 0 ? 'User' : i % 3 === 1 ? 'Answer' : 'KnowledgeSource',
    entity_id: i % 3 === 0 ? `user-${String(((i + 1) % 8) + 1).padStart(3, '0')}` : i % 3 === 1 ? `answer-${String((i % 15) + 1).padStart(3, '0')}` : `source-${String((i % 20) + 1).padStart(3, '0')}`,
    details: { timestamp: `2024-02-${String(1 + (i % 28)).padStart(2, '0')}T${String(9 + (i % 15)).padStart(2, '0')}:${String((i * 3) % 60).padStart(2, '0')}:00Z` },
    ip_address: `192.168.${Math.floor(i / 256)}.${i % 256}`,
    user_agent: `Mozilla/5.0 (${['Windows', 'Mac', 'Linux'][i % 3]}) AppleWebKit/${537 + (i % 10)} Chrome/${122 + (i % 5)}`),
    created_at: `2024-02-${String(1 + (i % 28)).padStart(2, '0')}T${String(9 + (i % 15)).padStart(2, '0')}:${String((i * 3) % 60).padStart(2, '0')}:00Z`,
  })) as AuditLog[],
};

export default mockData;