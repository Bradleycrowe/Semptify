"""
Dakota County Eviction Defense - Internationalization Service
Supports: English (EN), Spanish (ES), Somali (SO), Arabic (AR)
"""

from typing import Dict, Optional

# Primary language strings - English as base
STRINGS: Dict[str, Dict[str, str]] = {
    # Navigation
    "nav_home": {
        "en": "Home",
        "es": "Inicio",
        "so": "Bogga Hore",
        "ar": "الرئيسية"
    },
    "nav_answer": {
        "en": "File Answer",
        "es": "Presentar Respuesta",
        "so": "Xaree Jawaab",
        "ar": "تقديم الرد"
    },
    "nav_counterclaim": {
        "en": "Counterclaim",
        "es": "Contrademanda",
        "so": "Dacwad Lid ah",
        "ar": "دعوى مضادة"
    },
    "nav_motions": {
        "en": "Motions",
        "es": "Mociones",
        "so": "Codsiyada",
        "ar": "الطلبات"
    },
    "nav_hearing": {
        "en": "Hearing Prep",
        "es": "Preparación para Audiencia",
        "so": "Diyaarinta Dhageysiga",
        "ar": "التحضير للجلسة"
    },
    "nav_forms": {
        "en": "Forms Library",
        "es": "Biblioteca de Formularios",
        "so": "Maktabadda Foomamka",
        "ar": "مكتبة النماذج"
    },
    "nav_zoom": {
        "en": "Zoom Court Helper",
        "es": "Ayuda para Audiencia por Zoom",
        "so": "Caawiyaha Maxkamadda Zoom",
        "ar": "مساعد المحكمة عبر زوم"
    },
    
    # Common Actions
    "btn_next": {
        "en": "Next Step",
        "es": "Siguiente Paso",
        "so": "Tallaabada Xigta",
        "ar": "الخطوة التالية"
    },
    "btn_back": {
        "en": "Go Back",
        "es": "Regresar",
        "so": "Dib u Noqo",
        "ar": "رجوع"
    },
    "btn_save": {
        "en": "Save Progress",
        "es": "Guardar Progreso",
        "so": "Kaydi Horumarka",
        "ar": "حفظ التقدم"
    },
    "btn_download": {
        "en": "Download PDF",
        "es": "Descargar PDF",
        "so": "Soo Deji PDF",
        "ar": "تحميل PDF"
    },
    "btn_print": {
        "en": "Print",
        "es": "Imprimir",
        "so": "Daabac",
        "ar": "طباعة"
    },
    "btn_submit": {
        "en": "Submit",
        "es": "Enviar",
        "so": "Dir",
        "ar": "إرسال"
    },
    "btn_cancel": {
        "en": "Cancel",
        "es": "Cancelar",
        "so": "Kansal",
        "ar": "إلغاء"
    },
    
    # Headings
    "title_main": {
        "en": "Dakota County Eviction Defense",
        "es": "Defensa contra Desalojo del Condado de Dakota",
        "so": "Difaaca Ka-saarista Degmada Dakota",
        "ar": "الدفاع عن الإخلاء في مقاطعة داكوتا"
    },
    "title_answer": {
        "en": "File Your Answer to Eviction",
        "es": "Presente Su Respuesta al Desalojo",
        "so": "Xaree Jawaabta Aad Ku Bixinayso Ka-saarista",
        "ar": "قدم ردك على الإخلاء"
    },
    "title_counterclaim": {
        "en": "File a Counterclaim Against Your Landlord",
        "es": "Presente una Contrademanda Contra Su Arrendador",
        "so": "Xaree Dacwad Lid ah Mulkiilaha",
        "ar": "قدم دعوى مضادة ضد المالك"
    },
    "title_motions": {
        "en": "File a Motion",
        "es": "Presente una Moción",
        "so": "Xaree Codsi",
        "ar": "قدم طلب"
    },
    "title_hearing": {
        "en": "Prepare for Your Hearing",
        "es": "Prepárese para Su Audiencia",
        "so": "U Diyaarsanow Dhageysigaaga",
        "ar": "استعد لجلستك"
    },
    "title_zoom": {
        "en": "Zoom Court Appearance Guide",
        "es": "Guía para Audiencia por Zoom",
        "so": "Hagaha Muuqaalka Maxkamadda Zoom",
        "ar": "دليل المثول أمام المحكمة عبر زوم"
    },
    
    # Timeline/Deadlines
    "deadline_warning": {
        "en": "⚠️ You have {days} days to respond!",
        "es": "⚠️ ¡Tiene {days} días para responder!",
        "so": "⚠️ Waxaad haysataa {days} maalmood aad ku jawaabtid!",
        "ar": "⚠️ لديك {days} أيام للرد!"
    },
    "served_date": {
        "en": "When were you served with the eviction papers?",
        "es": "¿Cuándo le entregaron los documentos de desalojo?",
        "so": "Goorma laguu soo gaarsiiey waraaqaha ka-saarista?",
        "ar": "متى تم تبليغك بأوراق الإخلاء؟"
    },
    "hearing_date": {
        "en": "What is your hearing date?",
        "es": "¿Cuál es la fecha de su audiencia?",
        "so": "Muxuu yahay taariikhda dhageysigaaga?",
        "ar": "ما هو تاريخ جلستك؟"
    },
    
    # Defense Types
    "defense_nonpayment": {
        "en": "I couldn't pay rent because...",
        "es": "No pude pagar el alquiler porque...",
        "so": "Ma bixin karin kirada sababtoo ah...",
        "ar": "لم أتمكن من دفع الإيجار بسبب..."
    },
    "defense_habitability": {
        "en": "My landlord failed to maintain the property",
        "es": "Mi arrendador no mantuvo la propiedad",
        "so": "Mulkiilahaygu wuu ku guuldareystey inuu ilaaliy hantida",
        "ar": "فشل المالك في صيانة العقار"
    },
    "defense_retaliation": {
        "en": "This eviction is retaliation for...",
        "es": "Este desalojo es una represalia por...",
        "so": "Ka-saaristani waa aargoosi...",
        "ar": "هذا الإخلاء انتقام بسبب..."
    },
    "defense_improper_notice": {
        "en": "I was not properly served",
        "es": "No fui debidamente notificado",
        "so": "Si sax ah ii ma laga soo gaarsiiyin",
        "ar": "لم يتم تبليغي بشكل صحيح"
    },
    "defense_discrimination": {
        "en": "I believe this is discriminatory",
        "es": "Creo que esto es discriminatorio",
        "so": "Waxaan aaminsanahay inay tani tahay takoor",
        "ar": "أعتقد أن هذا تمييز"
    },
    "defense_rent_paid": {
        "en": "I already paid the rent",
        "es": "Ya pagué el alquiler",
        "so": "Kirada ayaan horay u bixiyey",
        "ar": "لقد دفعت الإيجار بالفعل"
    },
    
    # Counterclaim Reasons
    "counterclaim_repairs": {
        "en": "Landlord failed to make repairs",
        "es": "El arrendador no hizo las reparaciones",
        "so": "Mulkiilahu wuu ku guuldareystey inuu sameeyo dayactirka",
        "ar": "فشل المالك في إجراء الإصلاحات"
    },
    "counterclaim_deposit": {
        "en": "Landlord wrongfully withheld my security deposit",
        "es": "El arrendador retuvo injustamente mi depósito de seguridad",
        "so": "Mulkiilahu si khaldan ayuu u haystay lacagtayda dammaanadda",
        "ar": "احتجز المالك مبلغ التأمين بشكل غير قانوني"
    },
    "counterclaim_illegal_fees": {
        "en": "Landlord charged illegal fees",
        "es": "El arrendador cobró tarifas ilegales",
        "so": "Mulkiilahu wuxuu dalacay kharash sharci darro ah",
        "ar": "فرض المالك رسومًا غير قانونية"
    },
    "counterclaim_lockout": {
        "en": "Landlord illegally locked me out",
        "es": "El arrendador me cerró ilegalmente",
        "so": "Mulkiilahu si sharci darro ah ayuu igu xiray",
        "ar": "أغلق المالك علي الباب بشكل غير قانوني"
    },
    "counterclaim_utilities": {
        "en": "Landlord shut off utilities",
        "es": "El arrendador cortó los servicios",
        "so": "Mulkiilahu wuu xiray adeegyada guryaha",
        "ar": "قطع المالك المرافق"
    },
    
    # Motions
    "motion_dismiss": {
        "en": "Motion to Dismiss",
        "es": "Moción para Desestimar",
        "so": "Codsiga Joojinta",
        "ar": "طلب الرفض"
    },
    "motion_continuance": {
        "en": "Request for Continuance",
        "es": "Solicitud de Aplazamiento",
        "so": "Codsiga Dib u Dhigida",
        "ar": "طلب التأجيل"
    },
    "motion_stay": {
        "en": "Motion to Stay Writ",
        "es": "Moción para Suspender Orden",
        "so": "Codsiga Hakinta Amarka",
        "ar": "طلب وقف الأمر"
    },
    "motion_fee_waiver": {
        "en": "Fee Waiver Request",
        "es": "Solicitud de Exención de Tarifas",
        "so": "Codsiga Cafinta Kharashka",
        "ar": "طلب الإعفاء من الرسوم"
    },
    
    # Zoom Court
    "zoom_checklist": {
        "en": "Pre-Hearing Checklist",
        "es": "Lista de Verificación Pre-Audiencia",
        "so": "Liiska Hubinta Ka Hor Dhageysiga",
        "ar": "قائمة التحقق قبل الجلسة"
    },
    "zoom_tip_1": {
        "en": "Join 15 minutes early",
        "es": "Únase 15 minutos antes",
        "so": "Ku soo biir 15 daqiiqo horrayn",
        "ar": "انضم قبل 15 دقيقة"
    },
    "zoom_tip_2": {
        "en": "Test your audio and video",
        "es": "Pruebe su audio y video",
        "so": "Tijaabi codkaaga iyo muuqaalaada",
        "ar": "اختبر الصوت والفيديو"
    },
    "zoom_tip_3": {
        "en": "Have your documents ready to share",
        "es": "Tenga sus documentos listos para compartir",
        "so": "Diyaarso dukumentiyaadkaaga aad la wadaagtid",
        "ar": "جهز مستنداتك للمشاركة"
    },
    "zoom_tip_4": {
        "en": "Dress professionally",
        "es": "Vístase profesionalmente",
        "so": "U labis si xirfad leh",
        "ar": "ارتدِ ملابس رسمية"
    },
    "zoom_tip_5": {
        "en": "Find a quiet location",
        "es": "Encuentre un lugar tranquilo",
        "so": "Raadi meel aamusan",
        "ar": "ابحث عن مكان هادئ"
    },
    
    # Status Messages
    "status_saved": {
        "en": "Your progress has been saved",
        "es": "Su progreso ha sido guardado",
        "so": "Horumarka aad sameysay waa la keydiyey",
        "ar": "تم حفظ تقدمك"
    },
    "status_downloading": {
        "en": "Generating your document...",
        "es": "Generando su documento...",
        "so": "Waxaa la soo saaraya dokumentigaaga...",
        "ar": "جاري إنشاء المستند..."
    },
    "status_complete": {
        "en": "Complete! Download your packet below.",
        "es": "¡Completo! Descargue su paquete abajo.",
        "so": "Dhammaystiran! Soo deji baakadaada hoose.",
        "ar": "اكتمل! حمّل حزمتك أدناه."
    },
    
    # Error Messages
    "error_required": {
        "en": "This field is required",
        "es": "Este campo es obligatorio",
        "so": "Goobtan waa lagama maarmaan",
        "ar": "هذا الحقل مطلوب"
    },
    "error_invalid_date": {
        "en": "Please enter a valid date",
        "es": "Por favor ingrese una fecha válida",
        "so": "Fadlan geli taariikh sax ah",
        "ar": "يرجى إدخال تاريخ صحيح"
    },
    "error_server": {
        "en": "Something went wrong. Please try again.",
        "es": "Algo salió mal. Por favor intente de nuevo.",
        "so": "Wax baa qaldamay. Fadlan isku day mar kale.",
        "ar": "حدث خطأ ما. يرجى المحاولة مرة أخرى."
    },
    
    # Help Text
    "help_fee_waiver": {
        "en": "If you cannot afford court fees, you may qualify for a fee waiver (IFP).",
        "es": "Si no puede pagar las tarifas judiciales, puede calificar para una exención de tarifas (IFP).",
        "so": "Haddii aadan awoodin inaad bixiso kharashka maxkamadda, waad u qalmi kartaa cafinta kharashka (IFP).",
        "ar": "إذا لم تتمكن من تحمل رسوم المحكمة، فقد تكون مؤهلاً للإعفاء من الرسوم (IFP)."
    },
    "help_legal_aid": {
        "en": "Free legal help may be available. Call HomeLine: 612-728-5767",
        "es": "Puede haber ayuda legal gratuita disponible. Llame a HomeLine: 612-728-5767",
        "so": "Caawimo sharci oo bilaash ah ayaa la heli karaa. Wac HomeLine: 612-728-5767",
        "ar": "قد تتوفر مساعدة قانونية مجانية. اتصل بـ HomeLine: 612-728-5767"
    },
    
    # Footer
    "footer_disclaimer": {
        "en": "This tool provides legal information, not legal advice. For legal advice, consult an attorney.",
        "es": "Esta herramienta proporciona información legal, no asesoramiento legal. Para asesoramiento legal, consulte a un abogado.",
        "so": "Qalabkani wuxuu bixiyaa macluumaad sharci, ma aha talo sharci. Talo sharci, la tasho qareen.",
        "ar": "توفر هذه الأداة معلومات قانونية، وليس نصيحة قانونية. للحصول على نصيحة قانونية، استشر محاميًا."
    },
    "footer_emergency": {
        "en": "If you are being locked out RIGHT NOW, call 911",
        "es": "Si lo están encerrando AHORA MISMO, llame al 911",
        "so": "Haddii lagugu xirayo HADDA, wac 911",
        "ar": "إذا تم إغلاق الباب عليك الآن، اتصل بـ 911"
    }
}

def get_string(key: str, lang: str = "en", **kwargs) -> str:
    """Get translated string by key and language code."""
    if key not in STRINGS:
        return f"[Missing: {key}]"
    
    translations = STRINGS[key]
    lang = lang.lower()
    
    # Fallback chain: requested -> en
    text = translations.get(lang, translations.get("en", f"[No translation: {key}]"))
    
    # Format with kwargs if provided
    if kwargs:
        try:
            text = text.format(**kwargs)
        except KeyError:
            pass
    
    return text

def get_all_strings(lang: str = "en") -> Dict[str, str]:
    """Get all strings for a language (for template injection)."""
    return {key: get_string(key, lang) for key in STRINGS.keys()}

def get_supported_languages() -> list:
    """Return list of supported language codes."""
    return ["en", "es", "so", "ar"]

def get_language_names() -> Dict[str, str]:
    """Return language code to name mapping."""
    return {
        "en": "English",
        "es": "Español",
        "so": "Soomaali",
        "ar": "العربية"
    }

# RTL languages
RTL_LANGUAGES = {"ar"}

def is_rtl(lang: str) -> bool:
    """Check if language is right-to-left."""
    return lang.lower() in RTL_LANGUAGES
