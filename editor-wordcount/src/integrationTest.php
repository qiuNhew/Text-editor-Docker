<?php

class WordCountIntegrationTest {
    private $baseUrl = 'http://localhost:80';
    private $totalTests = 0;
    private $passedTests = 0;

    public function runTests() {
        echo "Starting Word Count Integration Tests\n";

        // Test successful word count
        $this->runTest(
            "Normal word count test",
            ['text' => 'hello world'],
            200,
            ['error' => false, 'answer' => 2]
        );

        // Test empty string
        $this->runTest(
            "Empty string test",
            ['text' => ''],
            400,
            ['error' => true]
        );

        // Test missing parameter
        $this->runTest(
            "Missing parameter test",
            [],
            400,
            ['error' => true]
        );

        // Test multiple spaces
        $this->runTest(
            "Multiple spaces test",
            ['text' => 'hello   world   test'],
            200,
            ['error' => false, 'answer' => 3]
        );

        // Print summary
        echo "\nIntegration Test Summary:\n";
        echo "Total Tests: {$this->totalTests}\n";
        echo "Passed Tests: {$this->passedTests}\n";

        return ($this->totalTests === $this->passedTests) ? 0 : 1;
    }

    private function runTest($name, $params, $expectedStatus, $expectedResponse) {
        $this->totalTests++;
        echo "\nRunning Integration Test: $name\n";

        $url = $this->baseUrl . '?' . http_build_query($params);
        
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_HEADER, true);

        $response = curl_exec($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        
        // Split header and body
        $headerSize = curl_getinfo($ch, CURLINFO_HEADER_SIZE);
        $body = substr($response, $headerSize);
        
        curl_close($ch);

        $success = true;
        
        // Check HTTP status
        if ($httpCode !== $expectedStatus) {
            echo "✗ FAILED: Expected status $expectedStatus, got $httpCode\n";
            $success = false;
        }

        // Check response content
        $responseData = json_decode($body, true);
        foreach ($expectedResponse as $key => $value) {
            if (!isset($responseData[$key]) || $responseData[$key] !== $value) {
                echo "✗ FAILED: Response mismatch for key '$key'\n";
                $success = false;
                break;
            }
        }

        if ($success) {
            echo "✓ PASSED\n";
            $this->passedTests++;
        }
    }
}

// Run the integration tests
$tester = new WordCountIntegrationTest();
exit($tester->runTests());