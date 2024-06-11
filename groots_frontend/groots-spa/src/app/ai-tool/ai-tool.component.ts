import { Component } from '@angular/core';
import { NgSelectModule } from '@ng-select/ng-select';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-ai-tool',
  standalone: true,
  imports: [NgSelectModule, FormsModule, CommonModule, HttpClientModule],
  templateUrl: './ai-tool.component.html',
  styleUrl: './ai-tool.component.css'
})

export class AiToolComponent {

  constructor(private http: HttpClient) {}

  isPromptSubmitted: boolean = false;
  isPromptSent: boolean = false;
  isContinuePressed: boolean = false;
  isLoading: boolean = false;
  isBusinessModelSelected: boolean = false;
  isBusinessPhaseSelected: boolean = false;
  response: any;
  parsedResponse: string[] = [];
  showReferences = false;
  
  inputPrompt: string = "";
  business_model: string | null = null;
  business_phase: string | null = null;
  selectedCountry: any = null;

  prompts: string[] = [];
  countries = [
    { id: 0, name: 'United States', gdelt_id: "US" },
    { id: 1, name: 'United Kingdom', gdelt_id: "UK" },
    { id: 2, name: 'Canada', gdelt_id: "Canada" },
  ];

  business_phases = [
    { id: 0, name: 'Design', key_val: "product_design_phase" },
    { id: 1, name: 'Production and Distribution', key_val: "production_and_distribution_phase" },
    { id: 2, name: 'Materials', key_val: "materials_phase" },
    { id: 3, name: 'End of Life', key_val: "end_of_life_phase" },
    { id: 4, name: 'Use', key_val: "use_phase" },
  ];

  /**
   * Handles the response from the server.
   * @param response The response from the server.
   */
  handleResponse(response: any): void {
    this.response = response;
    this.parseLlmResponse(response.llm_response);
  }

  /**
   * Parses the response from the language model.
   * @param llmResponse The response from the language model.
   */
  parseLlmResponse(llmResponse: string): void {
    this.parsedResponse = llmResponse.split('\n').filter(line => line.trim());
  }


   /**
   * Toggles the visibility of the references section.
   */
  toggleReferences(): void {
    this.showReferences = !this.showReferences;
  }

  selectBusinessModel(model: string): void {
    this.business_model = model
    this.isBusinessModelSelected = true;
  }

  /**
   * Selects the business phase.
   * @param phase The selected business phase.
   */
  selectBusinessPhase(phase: any): void {
    this.business_phase = phase.key_val;
    this.isBusinessPhaseSelected = true;
    this.sendPrompt();
  }

  /**
   * Handles the country selection change.
   * @param event The selection change event.
   */
  onCountryChange(event: any): void {
    console.log(this.countries[this.selectedCountry].gdelt_id);
  }

  /**
   * Submits the prompt entered by the user.
   * @param event The submission event.
   */
  submitPrompt(prompt: any): void {
    this.prompts.push(this.inputPrompt);
    this.isPromptSubmitted = true;
  }

  /**
   * Continues to the next step in the process.
   */
  onContinue(): void {
    this.isContinuePressed = true;
  }

  /**
   * Creates the prompt object to send to the server.
   * @returns The prompt object.
   */
  createPrompt(): any {
    var promptObject = {
      prompt: this.inputPrompt,
      country: this.countries[this.selectedCountry].gdelt_id,
      business_phase: this.business_phase,
      business_model: this.business_model,
      model: 'gpt-4'
    };

    return promptObject;
  }

  /**
   * Sends the prompt to the server.
   */
  sendPrompt(): any {
    var promptObject = this.createPrompt();

    this.http.post('http://127.0.0.1:5000/evaluate', promptObject, { headers: { 'Content-Type': 'application/json' } })
      .subscribe(
        (response: any) => {
          this.response = response;
          this.handleResponse(this.response);
          this.isLoading = false;
        },
        (error: any) => {
          console.error('Error:', error);
          this.isLoading = false;
        }
      );

    this.isPromptSent = true;
    this.isLoading = true;
  }
  
}
