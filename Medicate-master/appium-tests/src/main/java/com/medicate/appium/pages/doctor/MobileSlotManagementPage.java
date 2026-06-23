package com.medicate.appium.pages.doctor;

import io.appium.java_client.AppiumDriver;
import io.appium.java_client.pagefactory.AndroidFindBy;
import io.appium.java_client.pagefactory.iOSXCUITFindBy;
import com.medicate.appium.pages.MobileBasePage;
import org.openqa.selenium.WebElement;

public class MobileSlotManagementPage extends MobileBasePage {

    @AndroidFindBy(accessibility = "slot_date_picker")
    @iOSXCUITFindBy(accessibility = "slot_date_picker")
    private WebElement datePicker;

    @AndroidFindBy(accessibility = "slot_time_picker")
    @iOSXCUITFindBy(accessibility = "slot_time_picker")
    private WebElement timePicker;

    @AndroidFindBy(accessibility = "add_slot_btn")
    @iOSXCUITFindBy(accessibility = "add_slot_btn")
    private WebElement addSlotButton;

    @AndroidFindBy(accessibility = "slot_list_container")
    @iOSXCUITFindBy(accessibility = "slot_list_container")
    private WebElement slotListContainer;

    @AndroidFindBy(accessibility = "first_delete_slot_btn")
    @iOSXCUITFindBy(accessibility = "first_delete_slot_btn")
    private WebElement deleteSlotButton;

    public MobileSlotManagementPage(AppiumDriver driver) {
        super(driver);
    }

    public void clickDatePicker() {
        click(datePicker);
    }

    public void clickTimePicker() {
        click(timePicker);
    }

    public void clickAddSlot() {
        click(addSlotButton);
    }

    public boolean isSlotListVisible() {
        return isDisplayed(slotListContainer);
    }

    public void deleteFirstSlot() {
        click(deleteSlotButton);
    }
}
