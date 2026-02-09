import { useTranslation } from 'react-i18next'

export function useLanguage() {
    const { i18n } = useTranslation()

    const currentLang = i18n.language === 'zh-TW' ? 'ZH' : 'EN'

    const toggleLanguage = () => {
        const newLang = i18n.language === 'zh-TW' ? 'en' : 'zh-TW'
        i18n.changeLanguage(newLang)
    }

    return { currentLang, toggleLanguage, i18n }
}
