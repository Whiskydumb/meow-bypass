class TranslationManager:
    RUSSIAN = "Русский"
    ENGLISH = "English"
    KITTEN = "Kitten"
    
    _translations = {
        RUSSIAN: {
            "app_title": "meow bypass",
            "settings_title": "Настройки приложения",
            
            "method_label": "Метод:",
            "version_label": "Версия:",
            "language_label": "Язык:",
            "open_folder_btn": "Открыть папку",
            
            "method_1": "Метод 1",
            "method_2": "Метод 2",
            
            "release_version": "Релиз",
            "beta_version": "Бета",
            
            "open_action": "Открыть",
            "exit_action": "Выход",
            "settings_action": "Настройки",
            
            "play_button": "Запустить",
            "stop_button": "Остановить",
            
            "service_running": "Сервис запущен",
            "service_stopped": "Сервис не запущен",
            
            "admin_required_title": "Требуются права администратора",
            "admin_required_message": "Для работы WinDivert требуются права администратора. Перезапустить приложение с правами администратора?",
            "admin_required_status": "Требуются права администратора",
            "yes_button": "Да",
            "no_button": "Нет",
            
            "start_service_action": "Запустить сервис",
            "stop_service_action": "Остановить сервис",
            
            "service_started_notification": "Обход блокировок успешно запущен",
            "service_stopped_notification": "Обход блокировок остановлен",
        },
        ENGLISH: {
            "app_title": "meow bypass",
            "settings_title": "Application Settings",
            
            "method_label": "Method:",
            "version_label": "Version:",
            "language_label": "Language:",
            "open_folder_btn": "Open Folder",
            
            "method_1": "Method 1",
            "method_2": "Method 2",
            
            "release_version": "Release",
            "beta_version": "Beta",
            
            "open_action": "Open",
            "exit_action": "Exit",
            "settings_action": "Settings",
            
            "play_button": "Start",
            "stop_button": "Stop",
            
            "service_running": "Service is running",
            "service_stopped": "Service is not running",
            
            "admin_required_title": "Administrator privileges required",
            "admin_required_message": "WinDivert requires administrator privileges. Restart the application with administrator privileges?",
            "admin_required_status": "Administrator privileges required",
            "yes_button": "Yes",
            "no_button": "No",
            
            "start_service_action": "Start service",
            "stop_service_action": "Stop service",
            
            "service_started_notification": "Bypass successfully started",
            "service_stopped_notification": "Bypass stopped",
        },
        KITTEN: {
            "app_title": "meow bypass",
            "settings_title": "Purr-ferences Nya~",
            
            "method_label": "Meowthod:",
            "version_label": "Nya-version:",
            "language_label": "Languanya:",
            "open_folder_btn": "Open Litter Box",
            
            "method_1": "Mewthod 1 (Purr)",
            "method_2": "Mewthod 2 (Nyaa)",
            
            "release_version": "Stable Fish",
            "beta_version": "Spicy Beta",
            
            "open_action": "Pounce!",
            "exit_action": "Scram!",
            "settings_action": "Purr-ferences",
            
            "play_button": "NYA-START!",
            "stop_button": "NYA-STOP!",
            
            "service_running": "Meowchine purring!",
            "service_stopped": "Meowchine sleeping...",
            
            "admin_required_title": "Need alpha cat powers!",
            "admin_required_message": "Nyaa~ Need alpha cat powers to use WinDivert! Give me permissions?",
            "admin_required_status": "Need alpha cat powers!",
            "yes_button": "Meow-Yes!",
            "no_button": "Nya-No!",
            
            "start_service_action": "Start purring!",
            "stop_service_action": "Stop purring!",
            
            "service_started_notification": "Nya~ Bypass powers activated!",
            "service_stopped_notification": "Purring stopped, taking a catnap...",
        }
    }
    
    def __init__(self):
        self._current_language = self.RUSSIAN
    
    @property
    def current_language(self):
        return self._current_language
    
    @current_language.setter
    def current_language(self, language):
        if language in self._translations:
            self._current_language = language
    
    def get_translation(self, key):
        if key in self._translations[self._current_language]:
            return self._translations[self._current_language][key]
        return key
    
    def get_languages(self):
        return list(self._translations.keys())


translator = TranslationManager() 