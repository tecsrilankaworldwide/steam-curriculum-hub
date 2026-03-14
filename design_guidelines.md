{
  "brand": {
    "name": "Global STEAM Education Hub",
    "byline": "Education Reform Bureau · TEC Sri Lanka Worldwide",
    "attributes": [
      "professional",
      "educational",
      "trustworthy",
      "globally inclusive",
      "high-readability",
      "teacher-grade information architecture",
      "modern (but not playful)"
    ],
    "visual_personality": {
      "style_fusion": [
        "Swiss-style layout discipline (tight grid, strong typographic hierarchy)",
        "Bento-grid content discovery (lesson explorer + dashboards)",
        "Soft enterprise SaaS polish (muted surfaces, subtle depth)",
        "Light texture/noise for ‘human-made’ finish (very subtle)"
      ],
      "avoid": [
        "cartoon/playful illustration overload",
        "purple-heavy AI aesthetics",
        "dark saturated gradients",
        "centered-everything layouts"
      ]
    }
  },

  "inspiration_refs": {
    "sources": [
      {
        "type": "inspiration_search",
        "name": "Dribbble learning platform dashboards",
        "url": "https://dribbble.com/search/learning-platform-dashboard"
      },
      {
        "type": "inspiration_search",
        "name": "Dribbble elearning dashboard",
        "url": "https://dribbble.com/search/elearning-dashboard"
      },
      {
        "type": "inspiration_search",
        "name": "Behance e-learning platform ui",
        "url": "https://www.behance.net/search/projects/e-learning%20platform%20ui?locale=en_US"
      }
    ],
    "what_to_extract": [
      "Lesson library: left filter rail + search + sort + results grid/list toggle",
      "Student dashboard: progress overview + ‘continue learning’ + heatmap-style activity strip",
      "Admin dashboard: dense table patterns with bulk actions + status chips",
      "Language switcher: prominent, not buried; show native language name + English",
      "Bilingual reading: parallel columns + tab toggle + pinned glossary/tts bar"
    ]
  },

  "typography": {
    "fonts": {
      "heading": {
        "family": "Space Grotesk",
        "fallback": "ui-sans-serif, system-ui",
        "notes": "Modern, technical-but-friendly; reads well for STEM headings and dashboards."
      },
      "body": {
        "family": "IBM Plex Sans",
        "fallback": "ui-sans-serif, system-ui",
        "notes": "Highly legible for long bilingual lessons; strong multi-script support."
      },
      "mono": {
        "family": "IBM Plex Mono",
        "fallback": "ui-monospace, SFMono-Regular",
        "notes": "Use for code/ICT snippets, formulas, IDs."
      }
    },
    "google_fonts_import": {
      "instruction": "Add to /app/frontend/public/index.html <head> (preferred) or CSS import in index.css.",
      "links": [
        "https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap"
      ]
    },
    "scale": {
      "h1": "text-4xl sm:text-5xl lg:text-6xl font-semibold tracking-tight",
      "h2": "text-2xl sm:text-3xl font-semibold tracking-tight",
      "h3": "text-xl sm:text-2xl font-semibold",
      "subheading": "text-base md:text-lg text-muted-foreground",
      "body": "text-sm md:text-base leading-7",
      "small": "text-xs md:text-sm text-muted-foreground",
      "table": "text-sm leading-6",
      "notes": "Keep line-length 60–80 chars on desktop reading areas; use max-w-prose for lesson content."
    }
  },

  "color_system": {
    "intent": "Trustworthy academic + calm STEAM energy. Ocean-teal primary with slate neutrals; warm coral used sparingly for CTA and ‘contact for pricing’.",
    "gradient_policy": {
      "allowed": "Only background accents/decor (<= 20% viewport). Never on reading surfaces/cards. Use very mild, desaturated gradients.",
      "recommended_hero_bg": "Use subtle radial/linear wash behind hero headline only, then fade to solid background."
    },
    "tokens_css": {
      "instruction": "Replace :root tokens in /app/frontend/src/index.css with the following HSL values. Keep .dark optional; platform should default to light mode.",
      "css_variables": {
        "--background": "210 33% 98%",
        "--foreground": "222 35% 12%",
        "--card": "0 0% 100%",
        "--card-foreground": "222 35% 12%",
        "--popover": "0 0% 100%",
        "--popover-foreground": "222 35% 12%",

        "--primary": "188 72% 32%",
        "--primary-foreground": "210 40% 98%",

        "--secondary": "210 24% 95%",
        "--secondary-foreground": "222 35% 12%",

        "--muted": "210 24% 95%",
        "--muted-foreground": "215 16% 38%",

        "--accent": "171 42% 92%",
        "--accent-foreground": "222 35% 12%",

        "--destructive": "0 78% 56%",
        "--destructive-foreground": "210 40% 98%",

        "--border": "214 22% 88%",
        "--input": "214 22% 88%",
        "--ring": "188 72% 32%",

        "--chart-1": "188 72% 32%",
        "--chart-2": "26 84% 56%",
        "--chart-3": "222 35% 24%",
        "--chart-4": "171 42% 42%",
        "--chart-5": "43 92% 55%",

        "--radius": "0.9rem",

        "--brand-coral": "18 92% 60%",
        "--brand-ink": "222 35% 12%",
        "--brand-slate": "215 18% 46%",
        "--brand-mist": "210 33% 98%",
        "--brand-sand": "43 92% 95%"
      },
      "component_specific_tokens": {
        "--shadow-soft": "0 10px 30px -18px hsl(222 35% 12% / 0.25)",
        "--shadow-lift": "0 18px 50px -28px hsl(222 35% 12% / 0.35)",
        "--focus-outline": "0 0 0 4px hsl(188 72% 32% / 0.18)",
        "--surface-noise-opacity": "0.035"
      }
    },
    "gradients": {
      "hero_wash": "radial-gradient(80% 60% at 20% 10%, hsl(171 42% 92% / 0.9) 0%, transparent 60%), radial-gradient(70% 50% at 85% 15%, hsl(43 92% 95% / 0.9) 0%, transparent 55%)",
      "cta_accent": "linear-gradient(135deg, hsl(188 72% 32% / 0.14), hsl(171 42% 92% / 0.2))",
      "restriction_note": "Do not apply gradients to cards, tables, long lesson reading areas, or small UI elements."
    },
    "subject_color_tags": {
      "math": "hsl(188 72% 32%)",
      "physics": "hsl(222 35% 24%)",
      "chemistry": "hsl(26 84% 56%)",
      "biology": "hsl(171 42% 42%)",
      "technology": "hsl(197 55% 36%)",
      "engineering": "hsl(43 92% 55%)",
      "arts": "hsl(18 92% 60%)",
      "english": "hsl(215 16% 38%)",
      "ict": "hsl(160 45% 35%)"
    }
  },

  "layout_and_grid": {
    "global_container": {
      "max_width": "max-w-7xl",
      "page_padding": "px-4 sm:px-6 lg:px-8",
      "vertical_rhythm": "py-10 sm:py-12",
      "notes": "Avoid centering everything; use left-aligned reading flow."
    },
    "app_shell": {
      "desktop": "Left sidebar (collapsible) + top bar (search + language + user) + main content",
      "tablet": "Sidebar collapses into Sheet; top bar stays",
      "mobile": "Top bar + bottom nav (optional) + filters in Drawer"
    },
    "lesson_explorer_grid": {
      "pattern": "Filter rail (left) + results area (right). Results support grid (cards) and list (table-like).",
      "breakpoints": {
        "mobile": "Filters in Drawer; results in 1-col cards",
        "md": "Filters become Collapsible panel above results or left rail; 2-col cards",
        "lg": "Left rail fixed; 3-col cards"
      }
    },
    "lesson_detail_reading": {
      "max_width": "max-w-3xl for prose; additional right rail for glossary/tts on xl",
      "bilingual_modes": [
        "Tabs: Local | English | Side-by-side",
        "Side-by-side: two columns with independent line wrapping; keep shared scroll"
      ]
    },
    "rtl_support": {
      "approach": [
        "Set <html dir=\"rtl\"> or a top-level container dir prop when language is RTL.",
        "Use Tailwind logical utilities or conditional className to flip spacing: rtl:space-x-reverse etc (if rtl plugin), otherwise rely on CSS logical properties for paddings/margins.",
        "Avoid left/right absolute positioning; prefer inset-inline-start/end in custom CSS when needed."
      ],
      "must_work_for": ["Arabic", "Urdu", "Pashto"]
    }
  },

  "components": {
    "component_path": {
      "shadcn_ui_dir": "/app/frontend/src/components/ui",
      "primary_components_to_use": [
        "button.jsx",
        "input.jsx",
        "select.jsx",
        "tabs.jsx",
        "badge.jsx",
        "card.jsx",
        "table.jsx",
        "pagination.jsx",
        "navigation-menu.jsx",
        "breadcrumb.jsx",
        "dialog.jsx",
        "drawer.jsx",
        "sheet.jsx",
        "command.jsx",
        "scroll-area.jsx",
        "progress.jsx",
        "calendar.jsx",
        "sonner.jsx",
        "tooltip.jsx",
        "separator.jsx",
        "skeleton.jsx",
        "accordion.jsx",
        "collapsible.jsx"
      ]
    },

    "navigation": {
      "topbar": {
        "structure": [
          "Left: logo + org name",
          "Center (desktop): global search (Command-style)",
          "Right: language selector + notifications (optional) + user menu"
        ],
        "use": ["navigation-menu.jsx", "command.jsx", "dropdown-menu.jsx", "avatar.jsx"],
        "testids": {
          "global_search": "global-search-command",
          "language_menu": "language-selector",
          "user_menu": "user-menu"
        }
      },
      "sidebar": {
        "items": [
          "Home",
          "Lesson Explorer",
          "Student Dashboard",
          "Certificates",
          "Admin (role gated)"
        ],
        "use": ["sheet.jsx"],
        "micro_interaction": "Active item uses left accent bar (2px) + subtle background; hover uses muted surface shift."
      },
      "breadcrumb": {
        "use": ["breadcrumb.jsx"],
        "notes": "Always show curriculum/grade/subject path on Lesson Detail + Quiz."
      }
    },

    "lesson_cards": {
      "card_spec": {
        "use": ["card.jsx", "badge.jsx", "button.jsx", "progress.jsx"],
        "layout": "Title + subject chip + curriculum badges + grade + estimated time + progress bar (if started) + primary action (Continue/Start).",
        "states": {
          "default": "border-border bg-card",
          "hover": "shadow-[var(--shadow-soft)] border-foreground/10",
          "focus": "ring-2 ring-ring ring-offset-2",
          "locked": "show ‘Contact for Pricing’ badge + disabled start button"
        },
        "testids": {
          "card": "lesson-card",
          "start": "lesson-card-start-button",
          "pricing": "lesson-card-contact-pricing-button"
        }
      }
    },

    "filters": {
      "use": ["select.jsx", "input.jsx", "checkbox.jsx", "badge.jsx", "separator.jsx", "drawer.jsx"],
      "filters_required": [
        "Curriculum (Cambridge/Edexcel/ASDN)",
        "Grade (3-10)",
        "Subject (10)",
        "Difficulty (if applicable)",
        "Language availability"
      ],
      "pattern": "Sticky filter rail on lg; on mobile open Drawer with ‘Apply’ + ‘Reset’.",
      "testids": {
        "filter_curriculum": "lesson-filter-curriculum",
        "filter_grade": "lesson-filter-grade",
        "filter_subject": "lesson-filter-subject",
        "filter_search": "lesson-filter-search-input",
        "filter_apply": "lesson-filter-apply-button",
        "filter_reset": "lesson-filter-reset-button"
      }
    },

    "bilingual_content": {
      "controls": {
        "use": ["tabs.jsx", "toggle-group.jsx", "button.jsx", "tooltip.jsx"],
        "modes": [
          "Local only",
          "English only",
          "Bilingual side-by-side",
          "Bilingual inline (English line under Local line) — optional"
        ],
        "testids": {
          "mode_tabs": "bilingual-mode-tabs",
          "toggle_inline": "bilingual-inline-toggle"
        }
      },
      "reading_surface": {
        "spec": "Use a solid card/surface (bg-card) with max-w-prose; include sticky mini-toolbar for TTS + font size controls.",
        "avoid": "No gradients behind text blocks."
      }
    },

    "tts_controls": {
      "use": ["button.jsx", "slider.jsx", "select.jsx", "tooltip.jsx"],
      "required_controls": [
        "Play/Pause",
        "Stop",
        "Language voice selection (if available)",
        "Speed (0.8x–1.2x) slider",
        "Read Local / Read English buttons"
      ],
      "placement": [
        "Lesson Detail: sticky top-right (desktop) or sticky bottom bar (mobile)",
        "Quiz: optional read question button per question"
      ],
      "testids": {
        "tts_play": "tts-play-button",
        "tts_stop": "tts-stop-button",
        "tts_speed": "tts-speed-slider",
        "tts_voice": "tts-voice-select",
        "tts_read_local": "tts-read-local-button",
        "tts_read_english": "tts-read-english-button"
      }
    },

    "quiz_ui": {
      "use": ["card.jsx", "radio-group.jsx", "checkbox.jsx", "progress.jsx", "badge.jsx", "button.jsx", "alert.jsx", "tabs.jsx"],
      "layout": "Left: question + options. Right (desktop): progress + timer (optional) + difficulty chip + help/explanation accordion.",
      "feedback": {
        "instant": "On submit show inline Alert with explanation; highlight correct option with subtle green outline and incorrect with muted red outline (no harsh fills).",
        "scoring": "Show per-question points and overall progress bar."
      },
      "testids": {
        "quiz_next": "quiz-next-button",
        "quiz_prev": "quiz-prev-button",
        "quiz_submit": "quiz-submit-button",
        "quiz_option": "quiz-option",
        "quiz_explanation": "quiz-explanation"
      }
    },

    "dashboards": {
      "student": {
        "use": ["card.jsx", "tabs.jsx", "progress.jsx", "table.jsx", "badge.jsx", "calendar.jsx"],
        "cards": [
          "Overall progress (by subject)",
          "Recent lessons",
          "Quiz scores",
          "Certificates ready"
        ],
        "visualization": {
          "library": "recharts",
          "charts": [
            "Stacked bar by subject progress",
            "Line chart for weekly learning time",
            "Small donut for completion"
          ]
        },
        "testids": {
          "student-progress-overview": "student-progress-overview",
          "student-recent-lessons": "student-recent-lessons",
          "student-certificate-card": "student-certificate-card"
        }
      },
      "admin": {
        "use": ["table.jsx", "tabs.jsx", "dialog.jsx", "select.jsx", "input.jsx", "badge.jsx", "dropdown-menu.jsx"],
        "tables": [
          "Lessons: status, curriculum, grade, subject, language coverage, last updated",
          "Inquiries: name, org, email, message, status, assigned"
        ],
        "patterns": [
          "Bulk actions (approve/publish/archive)",
          "Row actions via dropdown menu",
          "Inline status badge + filters"
        ],
        "testids": {
          "admin-lessons-table": "admin-lessons-table",
          "admin-inquiries-table": "admin-inquiries-table",
          "admin-lesson-create": "admin-lesson-create-button"
        }
      }
    },

    "inquiry_lead_gen": {
      "use": ["form.jsx", "input.jsx", "textarea.jsx", "select.jsx", "button.jsx", "card.jsx", "sonner.jsx"],
      "tone": "Commercial/professional. The CTA says ‘Contact for Pricing’ and ‘Request a Demo’.",
      "testids": {
        "inquiry-form": "inquiry-form",
        "inquiry-submit": "inquiry-submit-button"
      }
    },

    "licensing_attribution": {
      "use": ["alert.jsx", "accordion.jsx", "tooltip.jsx"],
      "spec": "At bottom of lesson detail: collapsible ‘Attribution & Licensing’ with OpenStax CC BY 4.0 and CK-12 CC BY-NC 3.0 badges + links.",
      "testids": {
        "lesson-licensing": "lesson-licensing-section"
      }
    }
  },

  "motion_and_microinteractions": {
    "principles": [
      "Use motion to explain state changes (filter applied, quiz submitted, saved).",
      "Prefer 150–220ms for hover/focus, 220–360ms for enter/exit."
    ],
    "library": {
      "recommended": "framer-motion",
      "install": "npm i framer-motion",
      "use_cases": [
        "Lesson cards enter on filter change (stagger 20–40ms)",
        "Drawer/Sheet slide with spring (reduced motion respected)",
        "Quiz feedback: small ‘settle’ animation on explanation reveal"
      ]
    },
    "no_universal_transition_rule": "Never use transition: all. Only transition colors/shadows/opacity.",
    "tailwind_recipes": {
      "card_hover": "transition-shadow transition-colors duration-200 ease-out hover:shadow-[var(--shadow-soft)]",
      "button_press": "active:scale-[0.98] transition-colors duration-200",
      "focus_ring": "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
    }
  },

  "accessibility_and_inclusion": {
    "wcag": "Target WCAG AA.",
    "key_rules": [
      "Minimum body text contrast; never place text on gradients.",
      "Visible focus rings on all interactive elements.",
      "Respect prefers-reduced-motion; disable large entrance animations.",
      "Provide keyboard navigation for lesson cards, filters, quiz options.",
      "RTL mirroring must also flip icons where meaning depends on direction."
    ],
    "content_readability": [
      "Use max-w-prose and generous line-height for lessons.",
      "Add font-size toggle (A-, A, A+) stored per user.",
      "Use headings/TOC with anchor links for long lessons."
    ],
    "testids_policy": "All buttons, links, form inputs, menus, and key informational text must include data-testid in kebab-case describing role (not appearance)."
  },

  "i18n_and_rtl_implementation_notes": {
    "library": {
      "recommended": "react-i18next",
      "install": "npm i i18next react-i18next",
      "notes": "Store UI strings in JSON per language; lesson content can come from API with Local+English fields."
    },
    "bilingual_display_data_model": {
      "lesson_fields": [
        "title_en",
        "title_local",
        "content_en",
        "content_local",
        "language_code",
        "rtl (boolean derived from language)"
      ],
      "rendering": "Tabs control which fields to show; side-by-side uses a 2-col grid on lg and stacked on mobile."
    },
    "rtl_languages": ["ar", "ur", "ps"],
    "direction_switch": {
      "js_example": "const dir = isRtl(lang) ? 'rtl' : 'ltr'; document.documentElement.setAttribute('dir', dir);",
      "tailwind_note": "Prefer spacing utilities that don’t hardcode left/right; where needed, branch className by dir."
    }
  },

  "data_density_strategy": {
    "lesson_library": [
      "Default view = cards (friendly).",
      "Teacher/Admin toggle = list/table-like density (efficient scanning).",
      "Persist view choice per user."
    ],
    "tables": {
      "rules": [
        "Sticky header on desktop",
        "Row hover highlight",
        "Inline status chips",
        "Batch selection via checkbox",
        "Pagination always visible"
      ]
    }
  },

  "images": {
    "image_urls": [
      {
        "category": "home_hero",
        "description": "Hero visual: global education objects (globe + school tools). Use as subtle side image or blurred background card.",
        "url": "https://images.unsplash.com/photo-1709054172839-17880c040f22?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NjAzMzN8MHwxfHNlYXJjaHwxfHxnbG9iYWwlMjBlZHVjYXRpb24lMjBzdHVkZW50cyUyMGxlYXJuaW5nJTIwZGl2ZXJzZXxlbnwwfHx8fDE3NzI5ODk2MDR8MA&ixlib=rb-4.1.0&q=85"
      },
      {
        "category": "home_secondary",
        "description": "Secondary section visual: globe on table (works with curriculum/global message).",
        "url": "https://images.unsplash.com/photo-1601742638130-f76cbe00ad01?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NjAzMzN8MHwxfHNlYXJjaHwyfHxnbG9iYWwlMjBlZHVjYXRpb24lMjBzdHVkZW50cyUyMGxlYXJuaW5nJTIwZGl2ZXJzZXxlbnwwfHx8fDE3NzI5ODk2MDR8MA&ixlib=rb-4.1.0&q=85"
      },
      {
        "category": "global_trust",
        "description": "Flags image: use as faint, heavily blurred banner behind ‘20 languages’ trust section (ensure readability).",
        "url": "https://images.unsplash.com/photo-1651421479704-470a78eef530?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NjAzMzN8MHwxfHNlYXJjaHwzfHxnbG9iYWwlMjBlZHVjYXRpb24lMjBzdHVkZW50cyUyMGxlYXJuaW5nJTIwZGl2ZXJzZXxlbnwwfHx8fDE3NzI5ODk2MDR8MA&ixlib=rb-4.1.0&q=85"
      },
      {
        "category": "placeholder",
        "description": "Generic globe + pencils still life for empty states or marketing card background.",
        "url": "https://images.unsplash.com/photo-1638202950928-83a735a11058?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NjAzMzN8MHwxfHNlYXJjaHw0fHxnbG9iYWwlMjBlZHVjYXRpb24lMjBzdHVkZW50cyUyMGxlYXJuaW5nJTIwZGl2ZXJzZXxlbnwwfHx8fDE3NzI5ODk2MDR8MA&ixlib=rb-4.1.0&q=85"
      }
    ]
  },

  "page_blueprints": {
    "home": {
      "sections": [
        "Topbar (language + login)",
        "Hero: value prop + curriculum badges + primary CTA (Explore Lessons) + secondary CTA (Contact for Pricing)",
        "Bento: 10 subjects grid with chips",
        "How it works: Learn → Quiz → Track → Certificate",
        "Trust: Open licensing + attribution + global languages",
        "Footer: org/copyright"
      ],
      "hero_layout": "Left text, right image in a rounded card; hero background uses allowed subtle wash gradients only."
    },
    "lesson_explorer": {
      "sections": [
        "Top controls: search, sort, view toggle",
        "Filter rail/drawer",
        "Results grid/list with pagination",
        "Empty state with suggestions"
      ]
    },
    "lesson_detail": {
      "sections": [
        "Breadcrumb + meta (subject, grade, curriculum, time)",
        "Bilingual mode tabs",
        "Lesson content surface",
        "TTS toolbar",
        "Quiz CTA",
        "Attribution & Licensing accordion"
      ]
    },
    "quiz": {
      "sections": [
        "Progress header (question index + overall score)",
        "Question card + options",
        "Instant feedback alert + explanation accordion",
        "Next/Previous navigation"
      ]
    },
    "student_dashboard": {
      "sections": [
        "Overview cards",
        "Charts (recharts)",
        "Recent lessons table",
        "Certificates"
      ]
    },
    "admin_dashboard": {
      "sections": [
        "Tabs: Lessons | Inquiries",
        "Filterable tables",
        "Create/Edit dialogs",
        "Status chips"
      ]
    },
    "auth": {
      "layout": "Two-column on desktop: left brand/story + right form card; on mobile single card.",
      "use": ["card.jsx", "form.jsx", "input.jsx", "button.jsx", "separator.jsx"]
    },
    "certificate": {
      "layout": "Preview in Card with metadata; download PDF button.",
      "testids": {
        "download": "certificate-download-button"
      }
    }
  },

  "engineering_notes_for_js": {
    "file_convention": "This repo uses .js and shadcn ui already present in /components/ui; write new components in .js (not .tsx).",
    "data_testid_requirement": "Add data-testid to every interactive element: <Button data-testid=\"...\">, <Input data-testid=\"...\" /> etc. For custom wrappers, pass it through props.",
    "cleanup_note": "Remove default CRA App.css centered header styles; avoid .App { text-align:center }."
  },

  "instructions_to_main_agent": [
    "1) Update /app/frontend/src/index.css : replace the :root tokens with provided HSL set; keep gradients limited to hero decoration only.",
    "2) Remove or stop using /app/frontend/src/App.css CRA demo styles; ensure no centered container patterns are introduced.",
    "3) Build an AppShell layout (Topbar + Sidebar + Main) using shadcn Sheet/Dropdown/Command; ensure RTL direction switch is supported.",
    "4) Lesson Explorer must support: search input, curriculum/grade/subject filters, pagination, grid/list toggle, and fast empty states.",
    "5) Lesson Detail must support bilingual tabs + side-by-side mode, plus TTS toolbar using Web Speech API. Avoid gradients behind reading text.",
    "6) Quizzes: instant feedback + explanation accordion; use accessible radio/checkbox groups and clear scoring.",
    "7) Dashboards: integrate recharts for progress overview; keep charts minimal and readable.",
    "8) Ensure ALL interactive elements and key informational UI have data-testid (kebab-case role-based naming).",
    "9) Use sonner toasts for saves/submits; include success/error states for inquiry form and admin actions.",
    "10) Implement i18n with react-i18next; store user language preference and set document dir for RTL languages (ar/ur/ps)."
  ],

  "General UI UX Design Guidelines": [
    "- You must **not** apply universal transition. Eg: `transition: all`. This results in breaking transforms. Always add transitions for specific interactive elements like button, input excluding transforms",
    "- You must **not** center align the app container, ie do not add `.App { text-align: center; }` in the css file. This disrupts the human natural reading flow of text",
    "- NEVER: use AI assistant Emoji characters like`🤖🧠💭💡🔮🎯📚🎭🎬🎪🎉🎊🎁🎀🎂🍰🎈🎨🎰💰💵💳🏦💎🪙💸🤑📊📈📉💹🔢🏆🥇 etc for icons. Always use **FontAwesome cdn** or **lucid-react** library already installed in the package.json",
    "",
    " **GRADIENT RESTRICTION RULE**",
    "NEVER use dark/saturated gradient combos (e.g., purple/pink) on any UI element.  Prohibited gradients: blue-500 to purple 600, purple 500 to pink-500, green-500 to blue-500, red to pink etc",
    "NEVER use dark gradients for logo, testimonial, footer etc",
    "NEVER let gradients cover more than 20% of the viewport.",
    "NEVER apply gradients to text-heavy content or reading areas.",
    "NEVER use gradients on small UI elements (<100px width).",
    "NEVER stack multiple gradient layers in the same viewport.",
    "",
    "**ENFORCEMENT RULE:**",
    "    • Id gradient area exceeds 20% of viewport OR affects readability, **THEN** use solid colors",
    "",
    "**How and where to use:**",
    "   • Section backgrounds (not content backgrounds)",
    "   • Hero section header content. Eg: dark to light to dark color",
    "   • Decorative overlays and accent elements only",
    "   • Hero section with 2-3 mild color",
    "   • Gradients creation can be done for any angle say horizontal, vertical or diagonal",
    "",
    "- For AI chat, voice application, **do not use purple color. Use color like light green, ocean blue, peach orange etc",
    "",
    "</Font Guidelines>",
    "",
    "- Every interaction needs micro-animations - hover states, transitions, parallax effects, and entrance animations. Static = dead.",
    "",
    "- Use 2-3x more spacing than feels comfortable. Cramped designs look cheap.",
    "",
    "- Subtle grain textures, noise overlays, custom cursors, selection states, and loading animations: separates good from extraordinary.",
    "",
    "- Before generating UI, infer the visual style from the problem statement (palette, contrast, mood, motion) and immediately instantiate it by setting global design tokens (primary, secondary/accent, background, foreground, ring, state colors), rather than relying on any library defaults. Don't make the background dark as a default step, always understand problem first and define colors accordingly",
    "    Eg: - if it implies playful/energetic, choose a colorful scheme",
    "           - if it implies monochrome/minimal, choose a black–white/neutral scheme",
    "",
    "**Component Reuse:**",
    "\t- Prioritize using pre-existing components from src/components/ui when applicable",
    "\t- Create new components that match the style and conventions of existing components when needed",
    "\t- Examine existing components to understand the project's component patterns before creating new ones",
    "",
    "**IMPORTANT**: Do not use HTML based component like dropdown, calendar, toast etc. You **MUST** always use `/app/frontend/src/components/ui/ ` only as a primary components as these are modern and stylish component",
    "",
    "**Best Practices:**",
    "\t- Use Shadcn/UI as the primary component library for consistency and accessibility",
    "\t- Import path: ./components/[component-name]",
    "",
    "**Export Conventions:**",
    "\t- Components MUST use named exports (export const ComponentName = ...)",
    "\t- Pages MUST use default exports (export default function PageName() {...})",
    "",
    "**Toasts:**",
    "  - Use `sonner` for toasts\"",
    "  - Sonner component are located in `/app/src/components/ui/sonner.tsx`",
    "",
    "Use 2–4 color gradients, subtle textures/noise overlays, or CSS-based noise to avoid flat visuals."
  ]
}
