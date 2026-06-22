package com.medicate.appium.pages.shared;

import io.appium.java_client.AppiumDriver;
import io.appium.java_client.pagefactory.AndroidFindBy;
import io.appium.java_client.pagefactory.iOSXCUITFindBy;
import com.medicate.appium.pages.MobileBasePage;
import org.openqa.selenium.WebElement;

public class MobileAiChatPage extends MobileBasePage {

    @AndroidFindBy(accessibility = "chat_bubble_trigger")
    @iOSXCUITFindBy(accessibility = "chat_bubble_trigger")
    private WebElement chatBubbleTrigger;

    @AndroidFindBy(accessibility = "chat_input_field")
    @iOSXCUITFindBy(accessibility = "chat_input_field")
    private WebElement chatInputField;

    @AndroidFindBy(accessibility = "chat_send_btn")
    @iOSXCUITFindBy(accessibility = "chat_send_btn")
    private WebElement chatSendButton;

    @AndroidFindBy(accessibility = "chat_response_area")
    @iOSXCUITFindBy(accessibility = "chat_response_area")
    private WebElement chatResponseArea;

    @AndroidFindBy(accessibility = "chat_clear_btn")
    @iOSXCUITFindBy(accessibility = "chat_clear_btn")
    private WebElement chatClearButton;

    public MobileAiChatPage(AppiumDriver driver) {
        super(driver);
    }

    public void openChatWindow() {
        click(chatBubbleTrigger);
    }

    public void sendQuery(String query) {
        sendKeys(chatInputField, query);
        click(chatSendButton);
    }

    public String getLatestResponse() {
        return getText(chatResponseArea);
    }

    public void clearChat() {
        click(chatClearButton);
    }
}
