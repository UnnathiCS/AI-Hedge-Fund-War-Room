import { useState } from "react";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";

export interface UserInfo {
  name: string;
  gender: "male" | "female" | "other";
  expertise: "beginner" | "intermediate" | "advanced";
}

interface UserProfileProps {
  onUserInfoChange: (userInfo: UserInfo) => void;
  isDisabled?: boolean;
}

export default function UserProfile({ onUserInfoChange, isDisabled = false }: UserProfileProps) {
  const [userInfo, setUserInfo] = useState<UserInfo>({
    name: "",
    gender: "male",
    expertise: "beginner",
  });

  const handleNameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newUserInfo = { ...userInfo, name: e.target.value };
    setUserInfo(newUserInfo);
    onUserInfoChange(newUserInfo);
  };

  const handleGenderChange = (value: string) => {
    const newUserInfo = { ...userInfo, gender: value as "male" | "female" | "other" };
    setUserInfo(newUserInfo);
    onUserInfoChange(newUserInfo);
  };

  const handleExpertiseChange = (value: string) => {
    const newUserInfo = { ...userInfo, expertise: value as "beginner" | "intermediate" | "advanced" };
    setUserInfo(newUserInfo);
    onUserInfoChange(newUserInfo);
  };

  return (
    <Card className="glass-card p-4 mb-4">
      <div className="space-y-4">
        {/* Header */}
        <div>
          <h3 className="text-sm font-semibold text-foreground mb-3">Your Profile</h3>
          <p className="text-xs text-muted-foreground">Agents will tailor advice based on your profile</p>
        </div>

        {/* Name Input */}
        <div className="space-y-2">
          <Label htmlFor="name" className="text-xs font-medium">
            Your Name
          </Label>
          <Input
            id="name"
            type="text"
            placeholder="Enter your name"
            value={userInfo.name}
            onChange={handleNameChange}
            disabled={isDisabled}
            className="text-sm"
          />
        </div>

        {/* Gender Selection */}
        <div className="space-y-3">
          <Label className="text-xs font-medium">Gender</Label>
          <RadioGroup value={userInfo.gender} onValueChange={handleGenderChange} disabled={isDisabled}>
            <div className="flex items-center space-x-2">
              <RadioGroupItem value="male" id="male" />
              <Label htmlFor="male" className="text-sm font-normal cursor-pointer">
                Male (Agents will say "bro", "boss")
              </Label>
            </div>
            <div className="flex items-center space-x-2">
              <RadioGroupItem value="female" id="female" />
              <Label htmlFor="female" className="text-sm font-normal cursor-pointer">
                Female (Agents will say "girl", "boss")
              </Label>
            </div>
            <div className="flex items-center space-x-2">
              <RadioGroupItem value="other" id="other" />
              <Label htmlFor="other" className="text-sm font-normal cursor-pointer">
                Other (Agents will say "boss")
              </Label>
            </div>
          </RadioGroup>
        </div>

        {/* Expertise Selection */}
        <div className="space-y-3">
          <Label className="text-xs font-medium">Trading Experience</Label>
          <RadioGroup value={userInfo.expertise} onValueChange={handleExpertiseChange} disabled={isDisabled}>
            <div className="flex items-center space-x-2">
              <RadioGroupItem value="beginner" id="beginner" />
              <Label htmlFor="beginner" className="text-sm font-normal cursor-pointer">
                Beginner (Simple explanations, risk warnings)
              </Label>
            </div>
            <div className="flex items-center space-x-2">
              <RadioGroupItem value="intermediate" id="intermediate" />
              <Label htmlFor="intermediate" className="text-sm font-normal cursor-pointer">
                Intermediate (Balanced analysis, technical details)
              </Label>
            </div>
            <div className="flex items-center space-x-2">
              <RadioGroupItem value="advanced" id="advanced" />
              <Label htmlFor="advanced" className="text-sm font-normal cursor-pointer">
                Advanced (Deep analysis, contrarian insights)
              </Label>
            </div>
          </RadioGroup>
        </div>

        {/* Display Current Selection */}
        {userInfo.name && (
          <div className="mt-3 p-3 rounded-lg bg-secondary/50 border border-border">
            <p className="text-xs text-muted-foreground">
              ✅ <span className="font-semibold text-foreground">{userInfo.name}</span>
              {userInfo.gender === "male" && ' (using "bro", "boss")'}
              {userInfo.gender === "female" && ' (using "girl", "boss")'}
              {userInfo.gender === "other" && ' (using "boss")'}
              <br />
              📊 Level: <span className="font-semibold text-foreground capitalize">{userInfo.expertise}</span> trader
            </p>
          </div>
        )}
      </div>
    </Card>
  );
}
