<?php

require('functions.inc.php');

class WordCountTest {
    private $totalTests = 0;
    private $passedTests = 0;

    public function runTests() {
        echo "Starting Word Count Unit Tests\n";

        // Test normal case
        $this->runTest(
            "Normal text test",
            "there are four words",
            4
        );

        // Test multiple spaces
        $this->runTest(
            "Multiple spaces test",
            "there   are   four    words",
            4
        );

        // Test special characters
        $this->runTest(
            "Special characters test",
            "hello! world, how's it going?",
            5
        );

        // Test empty string exception
        $this->runTestException(
            "Empty string test",
            "",
            "Input string cannot be empty"
        );

        // Test null input exception
        $this->runTestException(
            "Null input test",
            null,
            "Input must be a string"
        );

        // Print summary
        echo "\nTest Summary:\n";
        echo "Total Tests: {$this->totalTests}\n";
        echo "Passed Tests: {$this->passedTests}\n";

        // Return exit code based on test results
        return ($this->totalTests === $this->passedTests) ? 0 : 1;
    }

    private function runTest($name, $input, $expected) {
        $this->totalTests++;
        echo "\nRunning Test: $name\n";
        
        try {
            $result = wordcount($input);
            if ($result === $expected) {
                echo "✓ PASSED\n";
                $this->passedTests++;
            } else {
                echo "✗ FAILED: Expected $expected, got $result\n";
            }
        } catch (Exception $e) {
            echo "✗ FAILED: Unexpected exception: " . $e->getMessage() . "\n";
        }
    }

    private function runTestException($name, $input, $expectedMessage) {
        $this->totalTests++;
        echo "\nRunning Test: $name\n";
        
        try {
            wordcount($input);
            echo "✗ FAILED: Expected exception was not thrown\n";
        } catch (Exception $e) {
            if ($e->getMessage() === $expectedMessage) {
                echo "✓ PASSED: Correct exception thrown\n";
                $this->passedTests++;
            } else {
                echo "✗ FAILED: Wrong exception message: " . $e->getMessage() . "\n";
            }
        }
    }
}

// Run the tests
$tester = new WordCountTest();
exit($tester->runTests());