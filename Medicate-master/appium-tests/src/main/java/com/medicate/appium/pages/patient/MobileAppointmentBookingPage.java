package com.medicate.appium.pages.patient;

import io.appium.java_client.AppiumDriver;
import io.appium.java_client.pagefactory.AndroidFindBy;
import io.appium.java_client.pagefactory.iOSXCUITFindBy;
import com.medicate.appium.pages.MobileBasePage;
import org.openqa.selenium.WebElement;

public class MobileAppointmentBookingPage extends MobileBasePage {

    @AndroidFindBy(accessibility = "hospital_select_list")
    @iOSXCUITFindBy(accessibility = "hospital_select_list")
    private WebElement hospitalSelectList;

    @AndroidFindBy(accessibility = "first_hospital_card")
    @iOSXCUITFindBy(accessibility = "first_hospital_card")
    private WebElement firstHospitalCard;

    @AndroidFindBy(accessibility = "doctor_select_list")
    @iOSXCUITFindBy(accessibility = "doctor_select_list")
    private WebElement doctorSelectList;

    @AndroidFindBy(accessibility = "first_doctor_card")
    @iOSXCUITFindBy(accessibility = "first_doctor_card")
    private WebElement firstDoctorCard;

    @AndroidFindBy(accessibility = "slot_select_list")
    @iOSXCUITFindBy(accessibility = "slot_select_list")
    private WebElement slotSelectList;

    @AndroidFindBy(accessibility = "first_slot_card")
    @iOSXCUITFindBy(accessibility = "first_slot_card")
    private WebElement firstSlotCard;

    @AndroidFindBy(accessibility = "symptoms_field")
    @iOSXCUITFindBy(accessibility = "symptoms_field")
    private WebElement symptomsField;

    @AndroidFindBy(accessibility = "book_appt_btn")
    @iOSXCUITFindBy(accessibility = "book_appt_btn")
    private WebElement bookApptButton;

    public MobileAppointmentBookingPage(AppiumDriver driver) {
        super(driver);
    }

    public void selectHospital() {
        click(firstHospitalCard);
    }

    public void selectDoctor() {
        click(firstDoctorCard);
    }

    public void selectSlot() {
        click(firstSlotCard);
    }

    public void enterSymptoms(String symptoms) {
        sendKeys(symptomsField, symptoms);
    }

    public void clickBookAppointment() {
        click(bookApptButton);
    }
}
