package com.medicate.framework.utils;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;

import java.util.List;

public class AccessibilityUtils {

    /**
     * Verifies that all target elements matching locator have aria-label or alt tags.
     */
    public static boolean verifyElementsHaveAriaOrAlt(WebDriver driver, By locator) {
        List<WebElement> elements = driver.findElements(locator);
        if (elements.isEmpty()) {
            return true;
        }

        for (WebElement element : elements) {
            String ariaLabel = element.getAttribute("aria-label");
            String alt = element.getAttribute("alt");
            String role = element.getAttribute("role");

            if ((ariaLabel == null || ariaLabel.trim().isEmpty()) &&
                (alt == null || alt.trim().isEmpty()) &&
                (role == null || role.trim().isEmpty())) {
                System.out.println("Accessibility failure: element lacks aria-label, alt, and role: " + element.getTagName());
                return false;
            }
        }
        return true;
    }
}
