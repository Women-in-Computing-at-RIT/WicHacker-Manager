import { Routes, Route } from "react-router-dom";
import PageNotFound from "../pages/404Page";
import WiCHacksLanding from "../pages/wichacksLanding";
import { ProtectedComponent } from "../hocs/protectedRoute";
import UserHomepage from "../pages/hackers/hackerLanding";
import { NewHackerForm } from "../pages/hackers/createNewUser";
import HackerApplication from "../pages/hackers/application";
import HackerApplicationView from "../pages/hackers/hackerApplicationView";
import LoadingView from "../pages/LoadingView";

export default function AppRoutes(){
    /*  Eventually add admin portal routes
        <Route path="/manage" element={<ProtectedComponent component={HackathonManagerLandingPage} />} />
            <Route path="/manage/applications" element={<ProtectedComponent component={ApplicationList} />} />
            <Route path="/manage/admin/signup" element={<ProtectedComponent component={NewAdminForm} />} />
     */
    return (
        <Routes>
            <Route path="/" element={<WiCHacksLanding />}/>
            <Route path="/user" element={<ProtectedComponent component={UserHomepage} />} />
            <Route path="/user/create" element={<ProtectedComponent component={NewHackerForm} />} />
            <Route path="/user/apply" element={<ProtectedComponent component={HackerApplication} />} />
            <Route path="/user/application" element={<ProtectedComponent component={HackerApplicationView} />} />
            <Route path="/auth" element={<LoadingView />} />
            <Route path="/notFound" element={<PageNotFound />} />
            <Route path="*" element={<PageNotFound />} />
            <Route path="*/*" element={<PageNotFound />} />
            <Route path="*/*/*" element={<PageNotFound />} />
        </Routes>
    )
}