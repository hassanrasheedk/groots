import { Routes } from '@angular/router';
import { HomePageComponent } from './home-page/home-page.component';
import { AiToolComponent } from './ai-tool/ai-tool.component';
import { AboutUsComponent } from './about-us/about-us.component';

export const routes: Routes = [
    {path: '', component: HomePageComponent},
    {path: 'ai-tool', component: AiToolComponent},
    {path: 'about-us', component: AboutUsComponent},
];