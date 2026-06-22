package com.medicate.framework.pages.shared;

import com.medicate.framework.pages.BasePage;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

public class AiChatAssistantPage extends BasePage {

    // Locators
    private final By chatInput = By.xpath("//input[contains(@placeholder, 'Ask') or contains(@placeholder, 'message') or @type='text']");
    private final By sendButton = By.xpath("//button[contains(@aria-label, 'Send') or contains(., 'Send')]");
    private final By chatMessages = By.xpath("//*[contains(@class, 'message-bubble') or contains(@aria-label, 'Reply') or contains(text(), 'Advice')]");
    private final By clearHistoryButton = By.xpath("//button[contains(., 'Clear') or contains(@aria-label, 'Clear')]");

    public AiChatAssistantPage(WebDriver driver) {
        super(driver);
    }

    public void sendMessage(String message) {
        sendKeys(chatInput, message);
        click(sendButton);
    }

    public boolean hasRepliesInChat() {
        return isElementVisible(chatMessages);
    }

    public String getLastReplyText() {
        return getText(chatMessages);
    }

    public void clearHistory() {
        click(clearHistoryButton);
    }
}
