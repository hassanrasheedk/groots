import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-home-page',
  standalone: true,
  imports: [],
  templateUrl: './home-page.component.html',
  styleUrls: ['./home-page.component.css']
})
export class HomePageComponent {
  constructor(private router: Router) {}

  onGetStartedClick(): void {
    // Handle the "Get Started" button click
    this.router.navigateByUrl('/ai-tool');
  }

  onLearnMoreClick(): void {
    // Handle the "Learn More" button click
    this.router.navigateByUrl('/about-us');
  }
}